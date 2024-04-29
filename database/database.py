from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DataAccessLayer:
    connection = None
    engine = None
    conn_string = None

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string)
        Base.metadata.create_all(bind=self.engine)
        self.connection = self.engine.connect()
