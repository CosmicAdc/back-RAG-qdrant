from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.bdd import crud
from app.schemas import schemas
from app.bdd import models
from app.bdd.postgres import get_db

router = APIRouter(
    prefix="/bdd",  tags=["Postgres"]
)

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.post("/users/verify-password")
def verify_password(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user or not crud.verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Password is valid"}

@router.delete("/delete-tema/{tema_name}")
async def delete_tema(tema_name: str, db: Session = Depends(get_db)):
    success = crud.delete_tema_by_name(db, tema_name)
    if success:
        return {"message": f"El tema '{tema_name}' ha sido eliminado correctamente."}
    else:
        raise HTTPException(status_code=404, detail="Tema no encontrado.")
    
@router.post("/create-tema/")
async def create_tema_endpoint(tema: schemas.TemaCreate, db: Session = Depends(get_db)):
    db_tema = crud.create_tema(db=db, tema=tema)
    return {"message": "Tema creado con éxito", "tema": db_tema}

@router.delete("/collection/{collection_name}")
def delete_collection(collection_name: str, db: Session = Depends(get_db)):
    success = crud.delete_collection_by_name(db, collection_name)
    if success:
        return {"message": "Collection and its temas deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Collection not found")
    
@router.get("/collections/")
def read_all_collections(db: Session = Depends(get_db)):
    return crud.get_all_collections(db)