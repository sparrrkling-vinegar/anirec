import os

from sqlalchemy.orm import sessionmaker

from database.database import DataAccessLayer
from database.models import *

DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]

SQLALCHEMY_DATABASE_URL = f'sqlite+pysqlcipher://:{DATABASE_PASSWORD}@/anirec.db?cipher=aes-256-cfb&kdf_iter=64000'
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
