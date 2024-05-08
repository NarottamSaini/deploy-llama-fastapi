## https://fastapi.tiangolo.com/tutorial/sql-databases/
'''
Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
But once we create an instance of the SessionLocal class, this instance will be the actual database session.
We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
To create the SessionLocal class, use the function sessionmaker:
'''
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./product.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./temp_product.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
) ## connect_args={"check_same_thread": False , needed only for SQLlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()