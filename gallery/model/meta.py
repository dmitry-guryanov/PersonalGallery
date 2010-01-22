"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Session', 'engine', 'metadata']

engine = None

Session = scoped_session(sessionmaker())

metadata = MetaData()

