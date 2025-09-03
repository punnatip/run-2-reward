# main.py

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Form
from fastapi.responses import RedirectResponse

# นำเข้าส่วนประกอบต่างๆ ที่เราสร้างไว้จากไฟล์อื่น
import models
from database import SessionLocal, engine

# สร้างตารางในฐานข้อมูล (ถ้ายังไม่มี)
models.Base.metadata.create_all(bind=engine)

# สร้าง instance ของ FastAPI
app = FastAPI()

# ตั้งค่าให้ Jinja2Templates รู้จักโฟลเดอร์ templates
templates = Jinja2Templates(directory="templates")


# Dependency function สำหรับจัดการ database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# สร้าง Route (เส้นทาง URL) สำหรับหน้า activity log
@app.get("/activity")
def activity_log(request: Request, db: Session = Depends(get_db)):
    """
    ฟังก์ชันนี้จะถูกเรียกเมื่อมีคนเข้าเว็บ http://127.0.0.1:8000/activity
    """
    # 1. ดึงข้อมูลทั้งหมดจากตาราง Reward
    rewards = db.query(models.Reward).all()

    # 2. ส่งข้อมูลไปแสดงผลในไฟล์ activity_log.html
    return templates.TemplateResponse(
        "activity_log.html",
        {
            "request": request,
            "rewards": rewards  # ส่งตัวแปร rewards เข้าไปใน template
        }
    )

# --- เพิ่มฟังก์ชันนี้เข้าไป ---
@app.get("/add-reward")
def add_reward_form(request: Request):
    """
    แสดงหน้าฟอร์มสำหรับเพิ่มของรางวัล
    """
    return templates.TemplateResponse("add_reward.html", {"request": request})


# (แนะนำ) สร้าง Route สำหรับหน้าแรก ให้ redirect ไปยังหน้า activity
@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/activity")


# --- เพิ่มฟังก์ชันนี้เข้าไป ---
@app.post("/add-reward")
def add_reward_submit(
    name: str = Form(...), 
    quantity: int = Form(...), 
    db: Session = Depends(get_db)
):
    """
    รับข้อมูลจากฟอร์มแล้วบันทึกลง DB
    """
    # 1. สร้าง object ของรางวัลใหม่จากข้อมูลที่รับมา
    new_reward = models.Reward(name=name, quantity=quantity)

    # 2. เพิ่มข้อมูลใหม่ลงใน session และบันทึกลงฐานข้อมูล
    db.add(new_reward)
    db.commit()

    # 3. Redirect กลับไปที่หน้า activity log
    return RedirectResponse(url="/activity", status_code=303)
