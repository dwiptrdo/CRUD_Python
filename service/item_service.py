from sqlalchemy.orm import Session
from model.item_model import Item as ItemModel
from model.schema_model import ItemCreate, ItemSearchParams  # Import from schemas
from model.user_model import User

def get_user_by_id(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.id == user_id).first()

def create_item(db: Session, item: ItemCreate):
    db_item = ItemModel(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: str):
    return db.query(ItemModel).filter(ItemModel.id == item_id).first()

def get_items_by_criteria(db: Session, params: ItemSearchParams):
    query = db.query(ItemModel)
    for field in params.searchBy:
        query = query.filter(getattr(ItemModel, field).ilike(f"%{params.search}%"))
    return query.all()

def update_item(db: Session, item_id: str, item: ItemCreate):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        return None
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: str):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
