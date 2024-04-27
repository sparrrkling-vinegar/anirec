from sqlalchemy.orm import sessionmaker

from database.database import DataAccessLayer

from database.models import *

SQLALCHEMY_DATABASE_URL = "sqlite:///./anirec.db"
dal = None
SessionLocal = None


def get_db(name=SQLALCHEMY_DATABASE_URL):
    global dal, SessionLocal
    if dal is None:
        dal = DataAccessLayer()
        dal.db_init(name)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dal.engine)
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
