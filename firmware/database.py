from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pdb;

Base = declarative_base()

engine = create_engine('sqlite:///firmware/firmware.db')
Base.metadata.bind = engine
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)()
