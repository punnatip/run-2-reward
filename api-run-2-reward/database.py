# database.py

import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker

# 1. อ่านค่า DATABASE_URL จาก Environment Variable
DATABASE_URL = os.getenv("DATABASE_URL")

# เตรียมตัวแปร connect_args ไว้ก่อน
connect_args = {}

# 2. ตรวจสอบและจัดการ URL
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
# 3. Fallback ไปใช้ SQLite ถ้าไม่มี DATABASE_URL (สำหรับ Local Development)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./local.db"
    # กำหนด connect_args สำหรับ SQLite เท่านั้น
    connect_args = {"check_same_thread": False}

# 4. สร้าง Engine และส่ง connect_args ที่ถูกต้องเข้าไป
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

# 5. (ปรับปรุง) สร้าง SessionLocal Factory เพื่อใช้ใน Dependency Injection
# นี่คือวิธีที่เป็นมาตรฐานสำหรับ FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. ฟังก์ชันสำหรับสร้างตาราง
def create_db_and_tables():
    # สร้างตารางทั้งหมดจาก Model ที่สืบทอดมาจาก SQLModel
    SQLModel.metadata.create_all(engine)