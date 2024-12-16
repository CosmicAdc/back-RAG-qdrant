from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.bdd.postgres import Base,engine

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    class Config:
        from_attributes=True
        orm_mode=True

class Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    temas = relationship("Tema", back_populates="collection", cascade="all, delete-orphan")
    class Config:
        from_attributes=True
        orm_mode=True

class Tema(Base):
    __tablename__ = 'temas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))

    collection = relationship("Collection", back_populates="temas")
    class Config:
        from_attributes=True
        orm_mode=True
    
Base.metadata.create_all(bind=engine)
