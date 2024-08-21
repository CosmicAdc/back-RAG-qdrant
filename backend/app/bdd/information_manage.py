from http.client import HTTPException
import json
from pathlib import Path
from typing import List
import uuid
from app.bdd.qdrant_manage import add_documents
from app.schemas.upload import UploadUrlSchema
from app.utils.utils import cleanTXT, translate
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document


async def process_urls(data: UploadUrlSchema):
    if not data.urls:
        raise HTTPException(status_code=400, detail="La lista de urls está vacía")
    docs = []
    loader = AsyncHtmlLoader(data.urls)
    documents = loader.load()
    html2text = Html2TextTransformer()
    documents = html2text.transform_documents(documents)
    for document in documents:
        metadata_values = {}
        if data.metadata is not None:
            if isinstance(data.metadata, list):
                for json_string in data.metadata:
                    json_object = json.loads(json_string)
                    metadata_values.update(json_object)
            else:
                metadata_values.update( data.metadata)
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
    print(docs)
    return await add_documents(list_documents=docs, collection_name=data.collection_name)
    
    
