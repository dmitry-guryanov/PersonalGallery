import gallery.config.environment

import sqlalchemy as sa
from sqlalchemy import orm, Column
from sqlalchemy.types import *


from gallery.model import meta

def resync():
	"""Renews SQLAlchemy session with current thread"""
	del sac.session_current.current

def flush():
	"""Flushes all changes to database"""
	sac.session.flush()


class Photo(object):
	pass

class Album(object):
	pass

def init_model(engine):
	"""Call me before using any of the tables or classes in the model."""

	sm = orm.sessionmaker(autoflush=True, transactional=True, expire_on_commit = True,  bind=engine)

	meta.engine = engine
	meta.Session = orm.scoped_session(sm)

	t_photos = sa.Table("photos", meta.metadata,
				Column('id', Integer, primary_key=True),
				Column('name', Unicode),
				Column('display_name', Unicode),
				Column('album_id', Integer),
				Column('created', DateTime),
				Column('width', Integer),
				Column('height', Integer),
				Column('hidden', Boolean))
	orm.mapper(Photo, t_photos)

	t_albums = sa.Table("albums", meta.metadata,
				Column('id', Integer, primary_key = True),
				Column('name', Unicode),
				Column('display_name', Unicode),
				Column('parent_id', Integer),
				Column('created', DateTime, default = sa.func.now()),
				Column('pos', Integer),
				Column('preview', Unicode),
				Column('descr', Unicode),
				Column('hidden', Boolean))
	orm.mapper(Album, t_albums)

