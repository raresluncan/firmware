"""Module for creating the Base class for mapper objects and also the engine
   for bidirectional use (create database/write or read dacabase)"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'firmware.db')

Base = declarative_base()

engine = create_engine('sqlite:///' + DATABASE_PATH)
Base.metadata.bind = engine

db_session = sessionmaker(bind=engine)()
