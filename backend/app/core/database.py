from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update with your MySQL connection string
DATABASE_URL = "mysql+pymysql://root:Himanshu@localhost:3306/Himanshu"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
