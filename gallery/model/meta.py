"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['Session', 'engine', 'metadata']

engine = None

Session = None

Base = declarative_base()
metadata = Base.metadata

