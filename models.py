# models.py

from typing import Optional
from sqlmodel import Field, SQLModel

class Reward(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    quantity: int