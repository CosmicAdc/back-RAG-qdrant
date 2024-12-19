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
    
    
    
async def process_uploaded_file(loader, metadata, check, collection_name, practice):
    documents = loader.load()
    docs = []
    metadata_values = {}

    if metadata is not None:
        if isinstance(metadata, str):
            metadata_object = json.loads(metadata)
        elif isinstance(metadata, dict):
            metadata_object = metadata
        else:
            raise TypeError("Metadata debe ser un str o un dict.")

        metadata_values.update(metadata_object)
    
    combined_content = ""  # Variable para almacenar contenido combinado si practice == 1

    for document in documents:
        if not document.page_content.strip():
            continue  
        metadata_values = {}
        if metadata is not None:
            if isinstance(metadata, list):
                for json_string in metadata:
                    try:
                        json_object = json.loads(json_string)
                        metadata_values.update(json_object)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
            else:
                metadata_values.update(metadata)

        # Obtener la metadata del documento y combinarla
        metadata_dict = document.metadata
        if metadata_dict is not None and isinstance(metadata_dict, dict):
            metadata_values.update(metadata_dict)

        # Generar un ID único
        id_unico = uuid.uuid4()
        metadata_values['id_file'] = str(id_unico)

        # Añadir la clave "PRACTICA" con el valor correspondiente
        metadata_values['PRACTICA'] = "SI" if practice == 1 else "NO"

        # Procesar el contenido del documento
        dc = str(document.page_content)
        if check == 1:
            newTxt = translate(str(dc))
            dc = newTxt
        dc = cleanTXT(dc)

        # Si practice == 1, combinar el contenido
        if practice == 1:
            combined_content += dc + "\n"  # Combinar con un separador de salto de línea
        else:
            # Crear un nuevo documento con la metadata actualizada
            newdoc = Document(page_content=dc, metadata=metadata_values)
            docs.append(newdoc)
    docs_split = text_splitter.split_documents(docs)
    # Si practice == 1, crear un solo documento
    if practice == 1:
        combined_doc = Document(page_content=combined_content.strip(), metadata=metadata_values)
        docs_split = [combined_doc]    

    if len(docs_split) == 0:
        return None

    # Añadir los documentos procesados
    return await add_documents(list_documents=docs_split, collection_name=collection_name)
