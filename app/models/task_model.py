from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from app.database.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(
    Integer,
    ForeignKey("users.id")
)
    owner = relationship(
    "User",
    back_populates="tasks"
)
    