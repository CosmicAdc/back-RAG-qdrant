from app.bdd.information_manage import process_urls
from app.schemas.schemas import UploadUrlSchema
from fastapi import HTTPException, Body, APIRouter
from fastapi.responses import JSONResponse
import json

from app.bdd.qdrant_manage import (
    get_all_collections,
    validate_existence_collection,
    create_collection,
    add_documents,
    delete_collection,
    delete_documents,
    get_all_documents_by_collection,
    update_documents,
)
from app.schemas.schemas_qdrant import (
    CollectionSchema,
    DeleteDocumentSchema,
    UpdateDocumentSchema,
)
from langchain_core.documents import Document

router = APIRouter(
    prefix="/qdrant",
    tags=["Qdrant"],
)

@router.post("/create_collection")
async def create_collection_endpoint(data: CollectionSchema = Body(...)):
    try:
        collection_name = data.collection_name
        result = create_collection(collection_name)
        return JSONResponse(content={"message": result}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)

@router.get("/validate_collection/{collection_name}")
async def validate_collection_endpoint(collection_name: str):
    try:
        result = validate_existence_collection(collection_name)
        return JSONResponse(content={"message": result}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


@router.delete("/delete_collection/{collection_name}")
async def delete_collection_endpoint(collection_name: str):
    try:
        result = delete_collection(collection_name)
        return JSONResponse(content={"message": result}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)

@router.delete("/delete_documents")
async def delete_documents_endpoint(data: DeleteDocumentSchema = Body(...)):
    try:
        collection_name = data.collection_name
        list_ids = data.list_ids
        result = delete_documents(list_ids, collection_name)
        return JSONResponse(content={"message": result}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)

@router.get("/get_all_documents/{collection_name}")
async def get_all_documents_endpoint(collection_name: str):
    try:
        result = get_all_documents_by_collection(collection_name)
        # Parse the JSON string into a Python dictionary
        result_dict = json.loads(result)
        return JSONResponse(content=result_dict, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


@router.put("/update_documents")
async def update_documents_endpoint(data: UpdateDocumentSchema = Body(...)):
    try:
        collection_name = data.collection_name
        list_ids = data.list_ids

        if data.url:
            result = delete_documents(list_ids, collection_name)
            if not result:
                return JSONResponse(content={"message": "Error al eliminar documentos"}, status_code=500)
            upload_data = UploadUrlSchema(
                urls=[data.url],
                metadata=data.new_metadata,
                collection_name=collection_name,
                check=0  
            )
            result = await process_urls(upload_data)
            if result is not None:
                return JSONResponse(content={"message": "URL procesada correctamente"}, status_code=200)
            else:
                return JSONResponse(content={"message": "Error al procesar la URL"}, status_code=500)

        else:
            # Update with new_page_content
            document = Document(page_content=data.new_page_content, metadata=data.new_metadata)
            result = await update_documents(collection_name, list_ids, document)
            if result:
                return JSONResponse(content={"message": "Documentos actualizados correctamente"}, status_code=200)
            else:
                return JSONResponse(content={"message": "Error al actualizar documentos"}, status_code=500)

    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


@router.get("/get_all_collections")
async def get_all_collections_endpoint():
    try:
        return get_all_collections()
        return JSONResponse(content=result_dict, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


