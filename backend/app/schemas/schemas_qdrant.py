from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator
import json 


class CollectionSchema(BaseModel):
    collection_name: str = Field(..., description="Name of the collection to create")

class DeleteDocumentSchema(BaseModel):
    collection_name: str = Field(..., description="Name of the collection to delete documents from")
    list_ids: List[str] = Field(..., description="List of document IDs to delete")

class UpdateDocumentSchema(BaseModel):
    collection_name: str = Field(..., description="Name of the collection to update documents in")
    list_ids: List[str] = Field(..., description="List of document IDs to update")
    new_page_content: Optional[str] = Field(None, description="New page content for the document")
    url: Optional[str] = Field(None, description="URL to fetch content from")
    new_metadata: Optional[Dict[str, str]] = Field(None, description="New metadata for the document")


