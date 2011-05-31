import os, sys
import re

import shutil
import datetime, time
from logging import warn

from pyramid.security import Allow, Everyone, ALL_PERMISSIONS

import transaction

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation as relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.interfaces import MapperExtension, EXT_CONTINUE
from sqlalchemy.types import *

import sqlalchemy as sa

from zope.sqlalchemy import ZopeTransactionExtension

from gallery.lib.utils import *
from gallery.lib import config

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

#
# Static resource tree:
# MyApp->(AlbumRoot, PhotoRoot, LoginRoot, ArticleRoot)
#

class IdObject(object):
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, 'admin', ALL_PERMISSIONS),
	]

	def __init__(self, parent):
		self.__parent__ = parent

	def __getitem__(self, key):
		session = DBSession()
		try:
			id = int(key)
		except (ValueError, TypeError):
			raise KeyError(key)

		objname = self.__name__.capitalize()
		objclass = getattr(sys.modules.get(__name__), objname)
		query = session.query(objclass).filter_by(id = id)

		try:
			item = query.one()
			item.__parent__ = self
			item.__name__ = str(key)
			return item
		except NoResultFound:
			raise KeyError(key)

class SimpleObject(object):
	def __init__(self, parent):
		self.__parent__ = parent

class AlbumRoot(IdObject):
	__name__ = "album"

class PhotoRoot(IdObject):
	__name__ = "photo"

class ArticleRoot(IdObject):
	__name__ = "article"

class LoginRoot(SimpleObject):
	__name__ = "login"

class MyApp(object):
	__name__ = ""
	__parent__ = None
	__children__ = {}

	def __init__(self):
		self.__children__["album"] = AlbumRoot(self)
		self.__children__["photo"] = PhotoRoot(self)
		self.__children__["article"] = ArticleRoot(self)
		self.__children__["login"] = LoginRoot(self)

		for key, val in self.__children__.items():
			setattr(self, key, val)

	def __getitem__(self, key):
		return self.__children__[key]

root = MyApp()

def get_root(req = None):
	return root

#
# Database objects
#	AlbumRoot->Album
#	PhotoRoot->Photo
#	ArticleRoot->Article
#

def resolve_dup_name(path):
	dirname, filename = os.path.split(path)
	name, ext = os.path.splitext(filename)

	i = 1
	while 1:
		new_name = "%s--%.3d%s" % (name, i, ext)
		new_path = os.path.join(dirname, new_name)
		if not os.access(new_path, os.F_OK):
			return (new_name, new_path)
		i += 1

class PhotoExtension(MapperExtension):
	def before_delete(self, mapper, connection, instance):
		instance.before_delete()

	def append_result(self, mapper, selectcontext, row,
				instance, result, *args, **flags):
		return instance.append_result()

class Photo(Base):
	__tablename__ = "photos"
	__mapper_args__ = {"extension": PhotoExtension()}
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, 'admin', ALL_PERMISSIONS),
	]

	id = Column(Integer, primary_key = True)
	name = Column(Unicode(256))
	display_name = Column(Unicode(256))
	album_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime)
	width = Column(Integer)
	height = Column(Integer)
	hidden = Column(Boolean, default = False)

	def __init__(self, name, album_id, image_data):
		self.name = unicode(name)
		self.album_id = album_id

		# save file
		photo_path = self.get_path()
		if os.access(photo_path, os.F_OK):
			self.name, photo_path = resolve_dup_name(photo_path)

		f = open(photo_path, "w")
		f.write(image_data)
		f.close()

		# make preview
		inf = get_photo_info(self)
		preview_file = self.get_preview_path()

		if inf.width > inf.height:
			crop_cmd = "%dx%d+%d+0" % (inf.height, inf.height,
						(inf.width - inf.height) / 2)
		else:
			crop_cmd = "%dx%d+0+%d" % (inf.width, inf.width,
						(inf.height - inf.width) / 8)

		cmd = "convert %s -strip -crop %s -resize %d %s" % \
			(photo_path, crop_cmd, preview_size, preview_file)
		os.system(cmd)

		self.width = inf.width
		self.height = inf.height
		if inf.exif.has_key("Create Date"):
			str_date = inf.exif["Create Date"]
			if re.match("\d+:\d+:\d+ \d+:\d+:\d+.\d+", str_date):
				str_date = str_date[:-3]
			cr_time = time.strptime(str_date, "%Y:%m:%d %H:%M:%S")
			cr_ts = time.mktime(cr_time)
			self.created = datetime.datetime.fromtimestamp(cr_ts)
		else:
			self.created = datetime.datetime.now()

	def before_delete(self):
		try:
			os.unlink(self.get_path())
		except OSError, e:
			warn(e)

		try:
			os.unlink(self.get_preview_path())
		except OSError, e:
			warn(e)

	def append_result(self):
		self.__name__ = str(self.id)
		self.__parent__ = get_root()["photo"]
		return EXT_CONTINUE

	def get_path(self):
		return os.path.join(config.config["permanent_store"],
					str(self.album_id), self.name)

	def get_preview_path(self):
		pr_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", self.name)
		return os.path.join(config.config["permanent_store"],
				str(self.album_id), "previews", pr_name)
	def get_web_path(self):
		return "%s/%s/%s" % (config.config["web_static_path"],
					str(self.album_id), self.name)

	def get_web_preview_path(self):
		pr_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", self.name)
		return "%s/%s/previews/%s" % (config.config["web_static_path"],
					str(self.album_id), pr_name)

class AlbumExtension(MapperExtension):
	def after_insert(self, mapper, connection, instance):
		instance.after_insert()

	def before_delete(self, mapper, connection, instance):
		instance.before_delete()

	def append_result(self, mapper, selectcontext, row,
				instance, result, *args, **flags):
		return instance.append_result()

class Album(Base):
	__tablename__ = "albums"
	__mapper_args__ = {"extension": AlbumExtension()}
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, 'admin', ALL_PERMISSIONS),
	]

	id = Column(Integer, primary_key = True)
	display_name = Column(Unicode(256))
	parent_id = Column(Integer, ForeignKey('albums.id'))
	created = Column(DateTime, default = sa.func.now())
	preview_id = Column(Integer,
		ForeignKey('photos.id', name = "qweqwe", use_alter = True))
	descr = Column(Unicode(4096))
	hidden = Column(Boolean, default = False)
	sort_by = Column(Integer)

	photos = relationship("Photo", order_by = "Photo.created",
				backref = "album",
				primaryjoin = Photo.album_id==id,
				cascade = "delete")

	albums = relationship("Album", order_by = "Album.created",
				backref = backref("parent", remote_side = [id]),
				cascade = "delete")

	preview = relationship("Photo",
				backref = backref("displayed_album",
					uselist = False, passive_deletes = True),
				foreign_keys = [preview_id],
				primaryjoin = preview_id==Photo.id,
				passive_deletes = True)

	def after_insert(self):
		os.mkdir(self.get_path())
		os.mkdir(self.get_preview_path())

	def before_delete(self):
		try:
			shutil.rmtree(self.get_path())
		except OSError, e:
			warn(e)

	def append_result(self):
		self.__name__ = str(self.id)
		self.__parent__ = get_root()["album"]
		return EXT_CONTINUE

	def get_path(self):
		return os.path.join(config.config["permanent_store"],
					str(self.id))

	def get_preview_path(self):
		return os.path.join(config.config["permanent_store"],
					str(self.id), "previews")

	def get_web_thumb(self):
		if self.preview:
			return self.preview.get_web_preview_path()
		else:
			return "/static/i/default-preview.jpg"

class ArticleExtension(MapperExtension):
	def after_insert(self, mapper, connection, instance):
		instance.__name__ = str(instance.id)
		instance.__parent__ = get_root()["article"]

	def append_result(self, mapper, selectcontext, row,
				instance, result, *args, **flags):
		instance.__name__ = str(instance.id)
		instance.__parent__ = get_root()["article"]
		return EXT_CONTINUE


class Article(Base):
	__tablename__ = "articles"
	__mapper_args__ = {"extension": ArticleExtension()}
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, 'admin', ALL_PERMISSIONS),
	]

	id = Column(Integer, primary_key = True)
	title = Column(Unicode(256))
	created = Column(DateTime, default = sa.func.now())
	body = Column(UnicodeText)
	hidden = Column(Boolean, default = False)

	def get_body(self):
		r = re.compile("(?:\r\n){2}")
		pars = r.split(self.body)
		s = "\n".join(map(lambda x: "<p>%s</p>" % x, pars))
		return s

def appmaker(engine, **settings):
	DBSession.configure(bind = engine)
	Base.metadata.bind = engine
	return get_root
