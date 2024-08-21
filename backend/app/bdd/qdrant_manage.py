from qdrant_client import QdrantClient,models
from langchain_qdrant import Qdrant
from qdrant_client.http.models import Distance, VectorParams
from langchain.text_splitter import CharacterTextSplitter
from app.models.models import embeddings
from langchain_core.documents import Document
from uuid import uuid4
from typing import List
import json

from langchain.chains.query_constructor.ir import (
    Comparator,
    Comparison,
    Operation,
    Operator,
    StructuredQuery,
)
from langchain_community.query_constructors.qdrant import QdrantTranslator
 
client = QdrantClient(
    host="localhost", port=6333
)

col_name="superprueba4"


def validate_existence_collection(collection_name:str):
    return client.collection_exists(collection_name=collection_name)


def create_collection(collection_name:str):
    try:
        if not validate_existence_collection(collection_name):
            client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            return "Colleción creada"
        else:
            return "Colleción ya existe"
    except Exception as e:
        return F"Ocurrio un error al crear la collección {e}"

def get_collection_vectorstore(collection_name:str):
    if validate_existence_collection(collection_name):
        return Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
        )
    else:
        print("no se encontro la collección")
        return None

async def add_documents(list_documents:List[Document],collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        ids = [str(uuid4()) for _ in range(len(list_documents))]
        vectorstore.add_documents(documents=list_documents, ids=ids)
        return "url procesadas correctamente"
    else: return vectorstore

def delete_collection(collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        client.delete_collection(collection_name=collection_name)
        return True
    else: return False

def delete_documents(list_ids:List[str],collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
       vectorstore.delete(ids=list_ids)
    else: return vectorstore
    
def format_data_documents(records):
    records_list, _ = records
    extracted_data = {}
    for record in records_list:
        extracted_data[record.id] = {
            'metadata': record.payload['metadata'],
            'page_content': record.payload['page_content']
        }
    
    return extracted_data

def get_all_documents_by_collection(collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        result= client.scroll(
            collection_name=collection_name,
        )
        results = format_data_documents(result)
        return json.dumps(results, indent=4)
    else: return vectorstore
    
async def update_documents(collection_name:str,list_ids:List[str],document:Document):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        try:
            client.overwrite_payload(
                collection_name=collection_name,
                payload={
                    "page_content": document.page_content,
                },
                points=list_ids,
            )
            print("actualizado correctamente")
            return True
        except Exception as e:
            print("error",e)
            return False
            
    else: return vectorstore
    

document_1 = Document(page_content="foo", metadata={"baz": "bar"})
document_2 = Document(page_content="thud", metadata={"bar": "baz"})
document_3 = Document(page_content="i will be deleted :(")
documents = [document_1, document_2, document_3]
ids_del=["39d445ac-23ef-4c2a-ab4a-57d096213d14"]

create_collection(col_name)
#add_documents(documents,col_name)
delete_documents(ids_del,col_name)
#print(get_all_documents_by_collection(col_name))
#delete_collection(col_name)
#print(create_collection(col_name))


def construct_comparisons(query_request):
    comparisons = []
    if query_request.metadata_values:
        for attribute, value in query_request.metadata_values.items():
            comparisons.append(
                Comparison(
                    comparator=Comparator.EQ,
                    attribute=attribute,
                    value=value,
                )
            )
    return comparisons

async def selfQueryng(request):

    query_request = request
    comparisons = construct_comparisons(query_request)

    operators_mapping = {
        "AND": Operator.AND,
        "OR": Operator.OR
    }
    operator_value = query_request.operator

    operator = operators_mapping[operator_value]
    if (len(comparisons)>1):
        _filter = Operation(operator=operator, arguments=comparisons)
        filtros = QdrantTranslator().visit_operation(_filter)
        return filtros
    filtros = QdrantTranslator().visit_comparison(comparisons[0])
    return filtros