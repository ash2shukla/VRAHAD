import os
import sys
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Gi(Base):
    __tablename__ = 'GiObjects'
    gi = Column(String, primary_key=True)
    GiObj = Column(String(2500), nullable=False)

engine = create_engine('sqlite:///keys.db')

Base.metadata.create_all(engine)
