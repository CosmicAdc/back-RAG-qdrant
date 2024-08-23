from typing import List
from langchain.chains import create_history_aware_retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from qdrant_client import models
from app.AI.chain import base_chain_esp,base_chain_en
from app.bdd.qdrant_manage import client,get_collection_vectorstore
from app.constants import constants as settings
from app.models.models import embeddings,VLLM
from app.AI.PROMPTS import contextualize_q_prompt_spanish,contextualize_q_prompt_english
from langchain_community.chat_message_histories import RedisChatMessageHistory


store = {}

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_embedding(text):
    response = embeddings.embed_query(text)
    return response

def apply_bm25(query,retriever,collection_name,filtros=None):
    qdrant=get_collection_vectorstore(collection_name)
    if filtros:
        documents_by_similarity = qdrant.similarity_search(query=query, k=5, filter=filtros)
    else:
        documents_by_similarity = qdrant.similarity_search(query=query, k=5)
    if len(documents_by_similarity)>0:
        bm25_retriever = BM25Retriever.from_documents(documents_by_similarity)
        bm25_retriever.k = 3
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, retriever], weights=[0.20, 0.8]
        )
        return ensemble_retriever|format_docs
    else: 
        return retriever


def get_chain(idiom:str):
    if idiom=="es":
        return base_chain_esp
    else:
        return base_chain_en
    

def get_retriever(collection_name:str,query:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        retriever = vectorstore.as_retriever(
        search_type=settings.SEARCH_TYPE,
        search_kwargs=settings.SEARCH_KWARGS,
        )
        retriever= apply_bm25(query,retriever,collection_name)
        return retriever
    else: return vectorstore
    

def get_retriever_with_keywords(collection_name: str, query: str, keywords: List[str], strict: bool = False):
    vectorstore = get_collection_vectorstore(collection_name)
    if vectorstore is not None:
        condition_type = "should" if strict else "must"
        
        keyword_filter = models.Filter(**{
            condition_type: [
                models.FieldCondition(
                    key="page_content",
                    match=models.MatchText(text=keyword)
                ) for keyword in keywords
            ]
        })
        
        response = client.search(
            collection_name=collection_name,
            query_vector=get_embedding(query),
            query_filter=keyword_filter,
            with_payload=["page_content"],
            limit=3
        )
        return response
    else:
        return vectorstore
    
    
def create_history_retriver(retriever,idiom:str):
    if idiom=="es":
        history_aware_retriever = create_history_aware_retriever(
            VLLM, retriever, contextualize_q_prompt_spanish
        )
    else:
        history_aware_retriever = create_history_aware_retriever(
            VLLM, retriever, contextualize_q_prompt_english
        )
    return history_aware_retriever    
    
def show(inputs):
    print(inputs)
    return inputs


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    store[session_id].messages = store[session_id].messages[-4:]
    return store[session_id]


def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=settings.REDIS_URL)


def create_chain_history(query:str,chain,session_id:str):
    conversational_rag_chain = RunnableWithMessageHistory(
        chain,
        get_message_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ) 
    print("final")
    
    return conversational_rag_chain.invoke({"input": query},config={"configurable": {"session_id": session_id}},  # constructs a key "abc123" in `store`.
    )["answer"]
    

def get_history_chat(session_id:str):
    from langchain_core.messages import AIMessage
    history = []  
    for message in store[session_id].messages:
        if isinstance(message, AIMessage):
            prefix = "AI"
        else:
            prefix = "User"
        history.append(f"{prefix}: {message.content}\n")  
        print(f"{prefix}: {message.content}\n") 
    return history  

        
# keywords = ["delet","sad","sadsf"]
# col_name="superprueba4"
# query="i will be deleted"

# get_retriever(col_name,query)

# get_retriever_with_keywords(col_name,query,keywords,strict=True)




