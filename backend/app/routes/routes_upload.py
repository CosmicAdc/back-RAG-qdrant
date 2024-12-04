from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Form, HTTPException, Body, APIRouter
from fastapi.responses import JSONResponse
from app.bdd.information_manage import process_uploaded_file, process_urls
from app.schemas.schemas import UploadUrlSchema  # Import the Pydantic schema
from fastapi import File,UploadFile,HTTPException
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader,UnstructuredURLLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
import json


ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx',"pptx"}

router = APIRouter(
    prefix="/upload",  tags=["Upload"]
)

@router.post("/upload_url")
async def upload_url(data: UploadUrlSchema = Body(...)):
    try:
        result = await process_urls(data)
        if result == []:
            return JSONResponse(content={"message": "Esta URL no se puede procesar intenta con otra o sube la información por otro medio"}, status_code=500)
        elif result is not None:
            return JSONResponse(content={"message": "URLs procesadas correctamente"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Error al procesar las URLs"}, status_code=500)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/uploadfiles")
async def create_upload_files(
    files: List[UploadFile] = File(...),
     metadata: Optional[str] = Form(None),
    traducir: int = Form(...),
    collection_name: str = Form(...)
):
    check = int(traducir)

    # Intentar deserializar metadata desde JSON
    try:
        metadata_dict = json.loads(metadata) if metadata else {}
        if not isinstance(metadata_dict, dict):
            raise ValueError("metadata no es un diccionario válido")
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="metadata debe ser un JSON válido")

    for file in files:
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos pdf, txt o docx")

        file_path = f"app/static/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        if file.filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file.filename.endswith('.txt'):
            loader = TextLoader(file_path)
        elif file.filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        elif file.filename.endswith('.pptx'):
            loader = UnstructuredPowerPointLoader(file_path)
        else:
            raise HTTPException(status_code=400, detail="Tipo de archivo no compatible")

        # Procesar el archivo cargado
        await process_uploaded_file(loader, metadata_dict, check, collection_name)

    return {"files_processed": len(files)}