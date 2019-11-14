from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///db.sqlite3')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    username = Column(String(length=20), unique=True, nullable=False)


Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)
