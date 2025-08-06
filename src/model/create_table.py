from models import Base
from database import engine
from sqlalchemy import create_engine
Base.metadata.create_all(bind=engine)
