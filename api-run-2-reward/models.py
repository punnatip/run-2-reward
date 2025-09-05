# models.py

from typing import Optional
from sqlmodel import Field, SQLModel

class Reward(SQLModel, table=True):
    __tablename__ = "reward"
    __table_args__ = {"extend_existing": True}  # ชั่วคราวให้ผ่าน deploy
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: int