from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.bdd.postgres import Base,engine

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Tema(Base):
    __tablename__ = "tema"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    collection_id = Column(Integer, ForeignKey("collections.id"))
    
Base.metadata.create_all(bind=engine)
