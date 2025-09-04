# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. กำหนดที่อยู่และชื่อไฟล์ของฐานข้อมูล SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./reward.db"

# 2. สร้าง Engine เพื่อเชื่อมต่อกับฐานข้อมูล
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. สร้าง SessionLocal เพื่อใช้ในการติดต่อกับฐานข้อมูลในแต่ละครั้ง
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. สร้าง Base class เพื่อให้ไฟล์ models ของคุณสืบทอดคุณสมบัติไปใช้
Base = declarative_base()