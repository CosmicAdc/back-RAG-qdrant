from typing import List
from app.bdd.qdrant_manage import client,get_collection_vectorstore
from app.constants import constants as settings
from app.models.models import embeddings

from qdrant_client import models


def format_docs(docs):
    return "\n\n".join(doc.payload["page_content"] for doc in docs)

def get_embedding(text):
    response = embeddings.embed_query(text)
    return response

def get_retriever(collection_name:str,query:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        retriever = vectorstore.as_retriever(
        search_type=settings.SEARCH_TYPE,
        search_kwargs=settings.SEARCH_KWARGS,
        )
        #print(retriever.invoke(query))
    else: return vectorstore
    



def get_retriever_with_keywords(collection_name: str, query: str, keywords: List[str], hybrid_search: bool = False):
    vectorstore = get_collection_vectorstore(collection_name)
    if vectorstore is not None:
        condition_type = "should" if hybrid_search else "must"
        
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
    
keywords = ["delet"]
col_name="superprueba4"
query="i will be deleted"

get_retriever(col_name,query)

get_retriever_with_keywords(col_name,query,keywords,hybrid_search=True)

