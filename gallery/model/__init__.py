import os
import re
from logging import info

import sqlalchemy as sa
from sqlalchemy import orm, Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.types import *

from gallery.model.meta import Session, Base

permanent_store = None
web_static_path = None

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

class AlbumExtension(MapperExtension):
	def after_insert(self, mapper, connection, instance):
		instance.after_insert()

class Album(Base):
	__tablename__ = "albums"
	__mapper_args__ = {"extension": AlbumExtension()}

	id = Column(Integer, primary_key = True)
	name = Column(Unicode(256))
	display_name = Column(Unicode(256))
	parent_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime, default = sa.func.now())
	pos = Column(Integer)
	preview = Column(Unicode(256))
	preview_id = Column(Integer, ForeignKey('photos.id', name = "qweqwe", use_alter = True))
	descr = Column(Unicode(4096))
	hidden = Column(Boolean)
	sort_by = Column(Integer)

	photos = relationship("Photo", order_by="Photo.created",
					backref = "album",
					primaryjoin = Photo.album_id==id)
	parent = relationship("Album", order_by="Album.created",
					backref = "albums", remote_side = [id])
	ppreview = relationship("Photo",
					backref=backref("displayed_album", uselist=False),
					foreign_keys = [preview_id],
					primaryjoin = preview_id==Photo.id)

	def after_insert(self):
		os.mkdir(self.get_path())
		os.mkdir(self.get_preview_path())

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

	permanent_store = config.get('permanent_store')
	web_static_path = config.get('web_static_path')

