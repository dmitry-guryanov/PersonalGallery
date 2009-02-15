import gallery.config.environment

import sqlalchemy as sa
from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *


from gallery.model import meta

def resync():
	"""Renews SQLAlchemy session with current thread"""
	del sac.session_current.current

def flush():
	"""Flushes all changes to database"""
	sac.session.flush()

Base = declarative_base()
class Photo(Base):
	__tablename__ = "photos"

	id = Column(Integer, primary_key=True)
	name = Column(Unicode)
	display_name = Column(Unicode)
	album_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime)
	width = Column(Integer)
	height = Column(Integer)
	hidden = Column(Boolean)

	album = relation("Album", backref = backref("photos", order_by = id))

class Album(Base):
	__tablename__ = "albums"

	id = Column(Integer, primary_key = True)
	name = Column(Unicode)
	display_name = Column(Unicode)
	parent_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime, default = sa.func.now())
	pos = Column(Integer)
	preview = Column(Unicode)
	descr = Column(Unicode)
	hidden = Column(Boolean)

	albums = relation("Album")

def init_model(engine):
	"""Call me before using any of the tables or classes in the model."""

	sm = orm.sessionmaker(autoflush=True, transactional=True, expire_on_commit = True,  bind=engine)

	meta.engine = engine
	meta.Session = orm.scoped_session(sm)

