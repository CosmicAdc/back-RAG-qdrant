import bcrypt
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.bdd import models
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm import Session
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    db_user = models.User(username=user.username, password=hashed_password.decode('utf-8'))  
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_collections(db: Session):
    return db.query(models.Collection).all()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def create_collection(db: Session, collection: schemas.CollectionCreate):
    db_collection = models.Collection(name=collection.name)
    db.add(db_collection)  
    db.commit()
    db.refresh(db_collection)
    return db_collection

def create_tema(db: Session, tema: schemas.TemaCreate):
    db_tema = models.Tema(name=tema.name, collection_id=tema.collection_id)
    db.add(db_tema)
    db.commit()
    db.refresh(db_tema)
    return db_tema

def delete_tema_by_name(db: Session, tema_name: str):
    db_tema = db.query(models.Tema).filter(models.Tema.name == tema_name).first()
    if db_tema:
        db.delete(db_tema)  
        db.commit() 
        return True
    return False

def delete_collection_by_name(db: Session, collection_name: str):
    db_collection = db.query(models.Collection).filter(models.Collection.name == collection_name).first()
    
    if db_collection:
        db.delete(db_collection)
        db.commit()
        return True
    return False

def get_temas_by_collection_id(db: Session, collection_id: int):
    return db.query(models.Tema).filter(models.Tema.collection_id == collection_id).all()
