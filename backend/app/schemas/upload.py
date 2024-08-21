import json
from pydantic import BaseModel, Field
from pydantic import BaseModel, model_validator
from typing import List, Dict, Optional

class UploadUrlSchema(BaseModel):
    urls: List[str] = Field(..., description="Lista de URLs a procesar")
    metadata: Optional[Dict[str, str]] = Field(None, description="Metadatos adicionales para las URLs")
    collection_name: str = Field(..., description="Nombre de la colección a la que se agregarán los documentos")
    check: int = Field(0, description="Si se debe traducir el texto a español")
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value