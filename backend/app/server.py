import asyncio
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

from app.constants import constants
from app.bdd import qdrant_manage,information_manage
from app.AI.retriever import get_retriever_with_keywords
from app.routes import routes_upload as upload


app = FastAPI()
app.include_router(upload.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    import uvicorn
    asyncio.run(information_manage.execute()) 
    uvicorn.run(app, host="0.0.0.0", port=8100,loop="asyncio")
