from sqlalchemy import Column, String, Text
from config.database_postgre import Base  # Menggunakan impor absolut dari database.py
import uuid

def generate_id():
    return uuid.uuid4().hex

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, default=generate_id)
    name = Column(String(100), index=True)
    description = Column(Text, index=True)
