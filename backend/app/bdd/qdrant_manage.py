from qdrant_client import QdrantClient,models
from langchain_qdrant import Qdrant
from qdrant_client.http.models import Distance, VectorParams
from langchain.text_splitter import CharacterTextSplitter
from app.models.models import embeddings
from langchain_core.documents import Document
from uuid import uuid4
from typing import List
import json


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

def add_documents(list_documents:List[Document],collection_name:str):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        ids = [str(uuid4()) for _ in range(len(list_documents))]
        vectorstore.add_documents(documents=list_documents, ids=ids)
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
    
def update_documents(collection_name:str,list_ids:List[str],list_documents:List[Document]):
    vectorstore=get_collection_vectorstore(collection_name)
    if vectorstore!= None:
        try:
            delete_documents(list_ids,collection_name)
            add_documents(list_documents,collection_name)
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