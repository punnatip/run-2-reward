# models.py

from typing import Optional
from sqlmodel import Field, SQLModel

# กำหนดโครงสร้างตาราง rewards โดยการสร้าง Class ที่สืบทอดจาก SQLModel
class Reward(SQLModel, table=True):
    # __tablename__ จะถูกสร้างจากชื่อคลาสโดยอัตโนมัติ (เป็น "reward")
    # หากต้องการชื่ออื่น ให้กำหนด __tablename__ = "rewards" ที่นี่ได้

    # กำหนดคอลัมน์ต่างๆ โดยใช้ Type Annotation และ Field
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    quantity: int