from http.client import HTTPException
import json
from pathlib import Path
from typing import List
import uuid
from app.bdd.qdrant_manage import add_documents
from app.schemas.schemas import UploadUrlSchema
from app.utils.utils import cleanTXT, translate,text_splitter
from langchain_community.document_loaders import SeleniumURLLoader
from langchain_core.documents import Document

import nltk

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


async def process_urls(data: UploadUrlSchema):
    if not data.urls:
        raise HTTPException(status_code=400, detail="La lista de urls está vacía")
    docs = []
    loader = SeleniumURLLoader(urls =data.urls)
    documents = loader.load()
    print(documents)
    for document in documents:
        if not document.page_content.strip():
            continue  
        metadata_values = {}
        if data.metadata is not None:
            if isinstance(data.metadata, list):
                for json_string in data.metadata:
                    try:
                        json_object = json.loads(json_string)
                        print(f"JSON object: {json_object}")  # Print JSON object
                        metadata_values.update(json_object)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")  # Print error if JSON decoding fails
            else:
                metadata_values.update(data.metadata)
        metadata_dict = document.metadata
        if metadata_dict is not None and isinstance(metadata_dict, dict):
            metadata_values.update(metadata_dict)
        id_unico = uuid.uuid4()
        metadata_values['id_file'] = str(id_unico)
        dc = str(document.page_content)
        if data.check == 1:
            newTxt = translate(str(dc))
            dc = newTxt
        dc = cleanTXT(dc)
        newdoc =Document(page_content=dc, metadata=metadata_values)
        docs.append(newdoc)
    docs_split=text_splitter.split_documents(docs)
    if len(docs) == 0:
        return None
    return await add_documents(list_documents=docs_split, collection_name=data.collection_name)
    
    
    
