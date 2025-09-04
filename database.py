# main.py หรือ database.py

import os # 👈 Import 'os' เพื่ออ่านค่า environment variables
from sqlmodel import SQLModel, create_engine, Session

# 1. อ่านค่า DATABASE_URL จาก Environment Variable
# os.getenv() จะคืนค่า None ถ้าไม่พบตัวแปรนี้
database_url = os.getenv("DATABASE_URL")

# ‼️ ข้อควรระวัง: Render ให้ URL ที่ขึ้นต้นด้วย postgres://
# แต่ SQLAlchemy (ที่ SQLModel ใช้) ต้องการ postgresql://
# ดังนั้นเราต้องแก้ค่านี้ก่อน
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# 2. สร้าง Engine เพื่อเชื่อมต่อกับ Database
# ใส่ connect_args={} ที่ว่างเปล่าไว้ก่อนเพื่อความเข้ากันได้
engine = create_engine(database_url, echo=True, connect_args={})


# ฟังก์ชันสำหรับสร้างตารางทั้งหมด (ถ้ายังไม่มี)
def create_db_and_tables():
    # Import model ของคุณทั้งหมดมาก่อนบรรทัดนี้
    SQLModel.metadata.create_all(engine)


# ฟังก์ชันสำหรับสร้าง Session เพื่อคุยกับ Database
def get_session():
    with Session(engine) as session:
        yield session

# ส่วนอื่นๆ ของแอป FastAPI ของคุณ ...
# เช่น @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()