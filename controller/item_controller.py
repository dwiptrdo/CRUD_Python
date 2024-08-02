from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from service.item_service import create_item, get_item, get_items_by_criteria, update_item, delete_item
from config.database_postgre import get_db
from model.schema_model import ItemCreate, ItemSearchParams, Item  # Import from schemas
from utils.jwt import get_current_user
from typing import List

router = APIRouter()


@router.post("/", response_model=Item)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    return create_item(db, item)

@router.get("/{item_id}", response_model=Item)
def read_item(item_id: str, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/search", response_model=List[Item])
def search_items(params: ItemSearchParams, db: Session = Depends(get_db)):
    items = get_items_by_criteria(db, params)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.put("/{item_id}", response_model=Item)
def update_item_endpoint(item_id: str, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", response_model=Item)
def delete_item_endpoint(item_id: str, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
