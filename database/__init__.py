from database.database import engine, Base

from database.models import *

Base.metadata.create_all(bind=engine)
