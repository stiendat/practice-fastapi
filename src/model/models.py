from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    isbn = Column(String, primary_key=True)
    book_title = Column(String, nullable=False)
    book_author = Column(String)
    year_of_publication = Column(Integer)
    publisher = Column(String)
    image_url_s = Column(String)
    image_url_m = Column(String)
    image_url_l = Column(String)
    quantity = Column(Integer, default=0)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_changed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
