# create_db.py

# นำเข้าสิ่งที่จำเป็นจากไฟล์ database.py และ models.py ของคุณ
from database import Base, engine 
import models

# แจ้งให้ทราบว่ากำลังจะสร้างฐานข้อมูล
print("Creating database and tables...")

# คำสั่งนี้จะสร้างตารางทั้งหมดที่นิยามไว้ใน models.py
# โดยอ้างอิงจาก Base และ engine ที่ตั้งค่าไว้
Base.metadata.create_all(bind=engine)

print("Database and tables created successfully.")