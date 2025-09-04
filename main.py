# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import List, Optional
from sqlmodel import Field, SQLModel # Import เพิ่ม
from database import engine, SessionLocal # <--- คุณอาจจะมีบรรทัดนี้อยู่
from models import Reward, SQLModel
from schemas import RewardCreate, RewardRead 

# --- สร้าง Schema สำหรับ Input/Output ---
# Schema สำหรับรับข้อมูลตอนสร้าง (ไม่มี id)
class RewardCreate(SQLModel):
    name: str
    quantity: int

# Schema สำหรับส่งข้อมูลกลับ (มี id)
class RewardRead(SQLModel):
    id: int
    name: str
    quantity: int


# --- ส่วน Lifespan และ get_db (เหมือนเดิม) ---
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ที่แก้ไขแล้ว ---

@app.get("/")
def read_root():
    return {"message": "Welcome to Run2Reward API"}

# ใช้ RewardCreate สำหรับรับข้อมูล และ RewardRead สำหรับส่งข้อมูลกลับ
@app.post("/rewards/", response_model=RewardRead)
def create_reward(reward: RewardCreate, db: Session = Depends(get_db)):
    # สร้าง instance ของ Reward model จากข้อมูลที่รับมา
    db_reward = Reward.model_validate(reward)
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

# ใช้ List[RewardRead] เพื่อให้แน่ใจว่าข้อมูลที่ส่งกลับมีโครงสร้างที่ถูกต้อง
@app.get("/rewards/", response_model=List[RewardRead])
def read_rewards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rewards = db.query(Reward).offset(skip).limit(limit).all()
    return rewards

# (เพิ่ม) Endpoint สำหรับดึงข้อมูลรางวัลชิ้นเดียวตาม ID
@app.get("/rewards/{reward_id}", response_model=RewardRead)
def read_reward_by_id(reward_id: int, db: Session = Depends(get_db)):
    reward = db.get(Reward, reward_id)
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found")
    return reward