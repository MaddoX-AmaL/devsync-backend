from sqlalchemy import Column, Integer, String
from app.database.database import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    tasks = relationship(
    "Task",
    back_populates="owner"
)