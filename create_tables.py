from app.database.database import Base, engine
from app.models.user_model import User
from app.models.task_model import Task

print(Base.metadata.tables.keys())
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")