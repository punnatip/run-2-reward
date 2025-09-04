# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

# Import ส่วนประกอบต่างๆ จากไฟล์อื่น
# (ตรวจสอบให้แน่ใจว่า path ถูกต้อง เช่น .database, .models)
from database import engine, SessionLocal
from models import Reward, SQLModel # Import SQLModel และ Reward model ของคุณ

# --- ส่วนของการสร้างตาราง ---
# ใช้ Lifespan event แทน on_event("startup") ที่กำลังจะถูกยกเลิกในอนาคต
def create_db_and_tables():
    print("Creating database and tables...")
    SQLModel.metadata.create_all(engine)
    print("Database and tables created.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    create_db_and_tables()
    yield
    # Code to run on shutdown (ถ้ามี)

# --- สร้าง FastAPI app และกำหนด Lifespan ---
app = FastAPI(lifespan=lifespan)


# --- Dependency สำหรับจัดการ Database Session ---
# นี่คือ "วิธีเบิกและคืน" Session ที่ถูกต้อง
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---

# Endpoint หลัก (สำหรับทดสอบว่า Server ทำงานหรือไม่)
@app.get("/")
def read_root():
    return {"message": "Welcome to Run2Reward API"}


# Endpoint สำหรับสร้าง Reward (ตัวอย่าง)
# หมายเหตุ: เราควรใช้ Pydantic/SQLModel schema สำหรับรับข้อมูล (RewardCreate)
# และสำหรับส่งข้อมูลกลับ (RewardRead) เพื่อความปลอดภัยและเป็นระเบียบ
@app.post("/rewards/", response_model=Reward)
def create_reward(reward_data: Reward, db: Session = Depends(get_db)):
    # reward_data จะเป็น instance ของ Reward ที่ FastAPI สร้างจาก JSON ที่ส่งมา
    db.add(reward_data)
    db.commit()
    db.refresh(reward_data)
    return reward_data


# Endpoint สำหรับดึงข้อมูล Reward ทั้งหมด (ตัวอย่าง)
@app.get("/rewards/", response_model=list[Reward])
def read_rewards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rewards = db.query(Reward).offset(skip).limit(limit).all()
    return rewards