from app.db.database import Base, engine
from app.db.models import Repository


Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")