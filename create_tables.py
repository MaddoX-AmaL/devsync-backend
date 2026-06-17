from app.database.database import engine
from app.models.user_model import Base, User

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")