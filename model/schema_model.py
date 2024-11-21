from pydantic import BaseModel
from typing import List

# Skema Pydantic untuk validasi input dan output
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemSearchParams(BaseModel):
    search: str
    searchBy: List[str]

class Item(BaseModel):
    id: str
    name: str
    description: str

    class Config:
        from_attributes = True
