import os
import re

from logging import info

import sqlalchemy as sa
from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *

#from gallery.model import meta
from gallery.model.meta import Session, Base
#from meta import Base

permanent_store = None
web_static_path = None

def resync():
	"""Renews SQLAlchemy session with current thread"""
	del sac.session_current.current

def flush():
	"""Flushes all changes to database"""
	sac.session.flush()

class Photo(Base):
	__tablename__ = "photos"

	id = Column(Integer, primary_key=True)
	name = Column(Unicode(256))
	display_name = Column(Unicode(256))
	album_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime)
	width = Column(Integer)
	height = Column(Integer)
	hidden = Column(Boolean)

	def get_path(self):
		info("PHOTO")
		info("self: %s" % self)
		info("album_id: %s" % str(self.album_id))
		info("name: %s" % self.name)
		info("permanent_store: %s" % permanent_store)

		return os.path.join(permanent_store,
					str(self.album_id), self.name)

	def get_preview_path(self):
		pr_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", self.name)
		return os.path.join(permanent_store, str(self.album_id),
					"previews", pr_name)
	def get_web_path(self):
		return "%s/%s/%s" % (web_static_path,
					str(self.album_id), self.name)

	def get_web_preview_path(self):
		pr_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", self.name)
		return "%s/%s/previews/%s" % (web_static_path,
					str(self.album_id), pr_name)

class Album(Base):
	__tablename__ = "albums"

	id = Column(Integer, primary_key = True)
	name = Column(Unicode(256))
	display_name = Column(Unicode(256))
	parent_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime, default = sa.func.now())
	pos = Column(Integer)
	preview = Column(Unicode(256))
	descr = Column(Unicode(4096))
	hidden = Column(Boolean)
	sort_by = Column(Integer)

	def get_path(self):
		return os.path.join(permanent_store, str(self.id))

	def get_preview_path(self):
		return os.path.join(permanent_store, str(self.id), "previews")

	def get_web_thumb(self):
		return "%s/%s/previews/%s" % (web_static_path,
				self.id, "000-album-preview-preview.jpg")

def init_model(engine, config):
	"""Call me before using any of the tables or classes in the model."""
	global permanent_store
	global web_static_path

	Session.configure(bind=engine)

#	sm = orm.sessionmaker(bind=engine)

#	meta.engine = engine
#	meta.Session = orm.scoped_session(sm)
	print "config=%s" % str(config)
	permanent_store = config.get('permanent_store')
	web_static_path = config.get('web_static_path')

