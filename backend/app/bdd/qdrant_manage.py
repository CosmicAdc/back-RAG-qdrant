from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant, QdrantVectorStore
from qdrant_client.http.models import Distance, VectorParams
from app.models.models import embeddings
from langchain_core.documents import Document
from uuid import uuid4
from typing import List
import json
from app.schemas import schemas
from langchain.chains.query_constructor.ir import (
    Comparator,
    Comparison,
    Operation,
    Operator,
)
from langchain.retrievers.self_query.qdrant import QdrantTranslator
from app.bdd import crud
from sqlalchemy.orm import Session

client = QdrantClient(
    host="localhost", port=6333
)


def validate_existence_collection(collection_name:str):
    return client.collection_exists(collection_name=collection_name)


def create_collection(db:Session,collection_name:str):
    try:
        if not validate_existence_collection(collection_name):
            client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            collection_data = schemas.CollectionCreate(name=collection_name)  # Crear el objeto CollectionCreate
            if crud.create_collection(db,collection_data):
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
    
def get_collection_vectorstore_for_add(collection_name:str):
    if validate_existence_collection(collection_name):
        return QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=collection_name,
            url="http://localhost:6333",
            content_payload_key="content"
        )
    else:
        print("no se encontro la collección")
        return None

async def add_documents(list_documents:List[Document],collection_name:str):
    print(list_documents)
    vectorstore=get_collection_vectorstore_for_add(collection_name)
    print(vectorstore)
    if vectorstore!= None:
        ids = [str(uuid4()) for _ in range(len(list_documents))]
        vectorstore.add_documents(documents=list_documents, ids=ids)
        return "url procesadas correctamente"
    else: return vectorstore


    

def delete_collection(db:Session,collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        client.delete_collection(collection_name=collection_name)
        crud.delete_collection_by_name(db,collection_name)
        return True
    else: return False

def delete_documents(list_ids:List[str],collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
       vectorstore.delete(ids=list_ids)
       return True
    else: return vectorstore

def get_all_collections():
    collections = client.get_collections()
    return collections
    
def format_data_documents(records):
    records_list, _ = records
    extracted_data = {}
    for record in records_list:
        extracted_data[record.id] = {
            'metadata': record.payload['metadata'],
            'page_content': record.payload['content']
        }
    return extracted_data

def get_all_documents_by_collection(collection_name:str):
    vectorstore=get_collection_vectorstore_for_add(collection_name)
    if vectorstore!= None:
        result= client.scroll(
            collection_name=collection_name,
            limit=100000,
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
                    "metadata": document.metadata,
                },
                points=list_ids,
            )
            print("actualizado correctamente")
            return True
        except Exception as e:
            print("error",e)
            return False
            
    else: return vectorstore
    

def construct_comparisons(metadata):
    comparisons = []
    if metadata:
        for attribute, value in metadata.items():
            comparisons.append(
                Comparison(
                    comparator=Comparator.EQ,
                    attribute=attribute,
                    value=value,
                )
            )
    return comparisons

async def selfQueryng(metadata:dict, operator:str):
    comparisons = construct_comparisons(metadata)
    operators_mapping = {
        "AND": Operator.AND,
        "OR": Operator.OR
    }
    operator = operators_mapping[operator]
    if (len(comparisons)>1):
        _filter = Operation(operator=operator, arguments=comparisons)
        filtros = QdrantTranslator().visit_operation(_filter)
        return filtros
    filtros = QdrantTranslator().visit_comparison(comparisons[0])
    return filtros