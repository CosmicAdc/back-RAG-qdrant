from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator
import json 

class UploadUrlSchema(BaseModel):
    urls: List[str] = Field(..., description="List of URLs to process")
    metadata: Optional[Dict[str, str]] = Field(None, description="Aditional metadata for the URLs")
    collection_name: str = Field(..., description="Collection who will add documents")
    check: int = Field(0, description="Check to translate to spanish the content")

    @validator('metadata', pre=True)
    def validate_metadata(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for metadata")
        return value

class QuerySchema(BaseModel):
    query: str = Field(..., description="Question of user")
    metadata: Optional[Dict[str, str]] = Field(None, description="Metadata for filter information")
    operator: Optional[str] = Field(None, description="Operator for filter the metdata AND or OR")
    collection_name: str = Field(..., description="Name of the collection to do the search")
    session_id: str = Field(..., description="session ID")


