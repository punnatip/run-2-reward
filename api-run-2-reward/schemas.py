# schemas.py

from sqlmodel import SQLModel

# Schema for receiving data when creating a reward (no ID)
class RewardCreate(SQLModel):
    name: str
    quantity: int

# Schema for sending data back to the user (includes the ID)
class RewardRead(SQLModel):
    id: int
    name: str
    quantity: int