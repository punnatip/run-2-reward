# models.py

from sqlalchemy import Column, Integer, String
from database import Base  # นำเข้า Base จากไฟล์ database.py ที่เราสร้างไว้

# กำหนดโครงสร้างตาราง rewards โดยการสร้าง Class
class Reward(Base):
    __tablename__ = "rewards"  # ชื่อตารางในฐานข้อมูล

    # กำหนดคอลัมน์ต่างๆ ในตาราง
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)