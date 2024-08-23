from typing import Dict, List
from fastapi import FastAPI, HTTPException, Body, APIRouter
from fastapi.responses import JSONResponse
from app.bdd.information_manage import process_urls
from app.schemas.schemas import UploadUrlSchema  # Import the Pydantic schema

router = APIRouter(
    prefix="/upload",  tags=["Upload"]
)

@router.post("/upload_url")
async def upload_url(data: UploadUrlSchema = Body(...)):
    try:
        result = await process_urls(data)
        if result is not None:
            return JSONResponse(content={"message": "URLs procesadas correctamente"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Error al procesar las URLs"}, status_code=500)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)
