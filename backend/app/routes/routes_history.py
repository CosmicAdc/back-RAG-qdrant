from app.AI.retriever import create_chain_history, create_history_retriver, get_chain, get_history_chat, get_retriever
from app.bdd.qdrant_manage import selfQueryng
from app.schemas.schemas import QuerySchema
from app.utils.utils import detect_idiom
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from langchain.chains import create_retrieval_chain


router = APIRouter(
    prefix="/history",  tags=["History"]
)


@router.post("/chat_history")
async def get_sesion_history(session_id: str = Body(...)):
    try:
        response=get_history_chat(session_id)
        return JSONResponse(content={"message": f"Historial:\n {response}"}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)


@router.post("/response")
async def query_request(data: QuerySchema=Body(...)):
    try:
        filtros=None
        if not data.query:
            raise HTTPException(status_code=400, detail="La pregunta del usuario está vacía")
        if not data.collection_name:
            raise HTTPException(status_code=400, detail="El nombre de la colección está vacío")
        if not data.session_id:
            raise HTTPException(status_code=400, detail="El ID de la sesión está vacío")
        idiom = detect_idiom(data.query)
        if data.metadata and data.operator:
            filtros= await selfQueryng(data.metadata,data.operator)
        pre_retriever = get_retriever(data.collection_name, data.query,filtros)
        if pre_retriever is None:
            raise HTTPException(status_code=404, detail="La colección no existe")
        retriever = create_history_retriver(pre_retriever, idiom)
        chain = get_chain(idiom)
        rag_chain = create_retrieval_chain(retriever, chain)
        response = create_chain_history(data.query, rag_chain, data.session_id)
        print("response:", response) 
        return JSONResponse(content={"answer": response}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Error inesperado " + str(e)}, status_code=500)
