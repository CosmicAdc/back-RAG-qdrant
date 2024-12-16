from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.bdd import crud
from app.schemas import schemas
from app.models import models
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

@router.post("/users/verify-password/")
def verify_password(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user or not crud.verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Password is valid"}
