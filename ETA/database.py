from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DB_URL = "postgresql://postgres:meeto1904%40@localhost:5555/expense_db"

engine = create_engine(DB_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind = engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
         