from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pdb;
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'firmware.db')

Base = declarative_base()

engine = create_engine('sqlite:///' + DATABASE_PATH)
Base.metadata.bind = engine

db_session = sessionmaker(bind=engine)()
