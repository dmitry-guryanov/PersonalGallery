import os
import shutil
import tempfile
import types
import time
import mimetypes
import datetime
import zipfile

from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer

from webhelpers.paginate import Page

from gallery.models import Album, Photo, PhotoRoot, DBSession
from gallery.lib import utils

def r(s):
	return "gallery:templates/" + s

#
# Album context handling functions
#

@view_config(context = Album, renderer = r("album.mako"))
@view_config(context = Album, name = "page", renderer = r("album.mako"))
def view(album, req):
	s = DBSession()
	page = _get_page(req)
	albums = _get_albums(req, s, album, "page", page)
	photos = _get_photos(req, s, album, "page", page)[1]
	counts = _get_counts(req, s, album, albums)

	return dict(album = album, albums = albums, photos = photos,
			pnav = None, photo = None, counts = counts)


@view_config(context = Album, name = "allphotos",
			renderer = r("album-allphotos.mako"))
def allphotos(album, req):
	s = DBSession()
	page = _get_page(req)
	pager =  _get_photos(req, s, album, "allphotos", page)[1]
	return dict(album = album, photos = pager)


@view_config(context = Album, name = "new",
			renderer = r("album-edit.mako"), permission = "edit")
def new(album, req):
	return dict(album = album, new_album = True)


@view_config(context = Album, name = "edit",
			renderer = r("album-edit.mako"), permission = "edit")
def edit(album, req):
	return dict(album = album, new_album = False)


@view_config(context = Album, name = "commitedit",
			request_method = "POST", permission = "edit")
def commitedit(album, req):
	if not req.params.get("commit"):
		return HTTPFound(location = req.resource_url(album))

	s = DBSession()

	if req.params.get("new_album"):
		a = Album(parent_id = album.id)
		s.add(a)
		s.commit()
	else:
		a = album

	a.name = req.params.get("name")
	a.display_name = req.params.get("title")
	a.descr = req.params.get("description")
	a.hidden = bool(req.params.get("hide_album", 0))
	a.sort_by = int(req.params.get("sort_by", 1))

	new_thumb = req.params.get('album_thumbnail')
	print new_thumb, repr(new_thumb)
	if type(new_thumb) is types.InstanceType:
		old_preview = a.preview

		# add preview
		name = new_thumb.filename.lstrip(os.sep)
		preview = Photo(name, a.id, new_thumb.file.read())
		new_thumb.file.close()
		preview.hidden = True
		s.add(preview)
		s.commit()

		a.preview_id = preview.id
		if old_preview:
			s.delete(old_preview)

	s.commit()
	return HTTPFound(location = req.resource_url(a))


@view_config(context = Album, name = "commitdel", permission = "edit")
def commitdel(album, req):
	s = DBSession()

	parent = album.parent
	s.delete(album)
	s.commit()
	return HTTPFound(location = req.resource_url(parent))


@view_config(context = Album, name = "addphoto",
		renderer = r("album-addphoto.mako"), permission = "edit")
def addphoto(album, req):
	return dict(album = album)

@view_config(context = Album, name = "commitaddphoto",
		request_method = "POST", permission = "edit")
def commitaddphoto(album, req):
	s = DBSession()
	for i in range(20):
		new_photo = req.params.get('new_photo-%d' % i)
		if type(new_photo) is not types.InstanceType:
			continue
		photo_add_single(s, album, new_photo)
	return HTTPFound(location = req.resource_url(album))


def photo_add_single(s, album, new_photo):
	name = new_photo.filename.lstrip(os.sep)
	tp = mimetypes.guess_type(name)[0]

	if tp == "image/jpeg":
		photo = Photo(name, album.id, new_photo.file.read())
		new_photo.file.close()
		s.add(photo)
		s.commit()
	elif tp == "application/zip":
		add_archive(s, album, new_photo.file, arc_type = "zip")
	else:
		return "Unsupported type"
	return None

def add_archive(s, album, file, arc_type):
	z = zipfile.ZipFile(file)
	for fname in z.namelist():
		if mimetypes.guess_type(fname)[0] == "image/jpeg":
			photo = Photo(os.path.basename(fname), album.id, z.read(fname))
			s.add(photo)
			s.commit()

#
# Photo context handling functions
#

@view_config(context = Photo, renderer = r("album.mako"))
@view_config(context = Photo, name = "view", renderer = r("album.mako"))
def photo_view(photo, req):
	s = DBSession()

	album = photo.album
	page = _get_page(req)
	albums =  _get_albums(req, s, album, "page", page)
	all_ph, photos =  _get_photos(req, s, album, "page", page)
	counts = _get_counts(req, s, album, albums)

	pnav = PhotosNav(all_ph, photo.id)
	return dict(album = album, albums = albums, photos = photos,
			pnav = pnav, photo = photo, counts = counts)

@view_config(context = Photo, name = "getajax",
			renderer = r("album-getajax.mako"))
def photo_getajax(photo, req):
	s = DBSession()
	all_ph, photos = _get_photos(req, s, photo.album, "page", 1)

	pnav = PhotosNav(all_ph, photo.id)
	return dict(album = photo.album, photo = photo, pnav = pnav)

@view_config(context = Photo, name = "commitdel", permission = "edit")
def photo_commitdel(photo, req):
	s = DBSession()

	album = photo.album
	s.delete(photo)
	s.commit()
	return HTTPFound(location = req.resource_url(album))

@view_config(context = Photo, name = "edit",
			renderer = r("photo-edit.mako"), permission = "edit")
def photo_edit(photo, req):
	return dict(photo = photo)

@view_config(context = Photo, name = "commitedit",
			request_method = "POST", permission = "edit")
def photo_commitedit(photo, req):
	if not req.params.get("commit"):
		return HTTPFound(location = req.resource_url(photo.album))

	s = DBSession()
	photo.display_name = req.params.get("title")
	photo.hidden = bool(req.params.get("hide_photo", 0))
	s.commit()

	return HTTPFound(location = req.resource_url(photo.album))

#
# Helper functions
#

def _get_page(req):
	if not req.subpath:
		return 1
	try:
		page = int(req.subpath[0])
		return page
	except ValueError:
		return 1

def _get_albums(req, s, album, act, page):
	albums_q = s.query(Album).filter(Album.parent_id == album.id)
	# hide albums only for guests
	if not req.admin:
		albums_q = albums_q.filter(Album.hidden == False)

	def _get_page_url(page, partial = None):
		return req.resource_url(album, act, str(page))
					
	albums = Page(albums_q, page = page,
			items_per_page = 16, url = _get_page_url)
	return albums

def _get_photos(req, s, album, act, page):
	def _get_page_url(page, partial = None):
		return req.resource_url(album, act, str(page))
					
	photos_q = s.query(Photo).filter(Photo.album_id == album.id)
	# hide photos only for guests
	if not req.admin:
		photos_q = photos_q.filter(Photo.hidden == False)
	if album.sort_by == utils.SORT_BY_DATE:
		photos_q = photos_q.order_by(Photo.created)
	elif album.sort_by == utils.SORT_BY_DATE_DESC:
		photos_q = photos_q.order_by(Photo.created.desc())

	photos = photos_q.all()

	pg = Page(photos, page = page,
			items_per_page = 16, url = _get_page_url)

	return(photos, pg)

def _get_counts(req, s, album, albums):
	# get photo counts
	photo_counts = s.execute("SELECT albums.id AS aid, COUNT(*) FROM albums JOIN "
				"photos ON album_id = albums.id "
				"WHERE albums.parent_id = %d GROUP BY photos.album_id;" % int(album.id)).fetchall()
	photo_counts = dict(photo_counts)

	# get album counts
	album_counts = s.execute("SELECT albums1.id AS aid, COUNT(*) AS count "
					"FROM albums albums1 JOIN albums albums2 ON "
					"albums2.parent_id = albums1.id "
					"WHERE albums1.parent_id = %d and (albums2.hidden = 0 or %d) "
					"GROUP BY albums2.parent_id;" % (int(album.id), int(req.admin))).fetchall()
	album_counts = dict(album_counts)

	counts = {}
	for a in albums:
		counts[a.id] = (album_counts.get(a.id, 0), photo_counts.get(a.id, 0))
	return counts


class PhotosNavError(Exception):
	pass

class PhotosNav:
	photo = None
	index = None
	first = None
	prev = None
	next = None
	last = None
	count = None

	def __init__(self, photos, pid):
		"""
		photos: list of Photo objects
		pid: current photo id
		"""
		photo_ids = map(lambda x: x.id, photos)

		if pid not in photo_ids:
			raise PhotosNavError("There is no photo %d" % pid)

		self.index = photo_ids.index(long(pid))

		if self.index != 0:
			self.prev = photos[self.index - 1]
			self.first = photos[0]

		if self.index != len(photo_ids) - 1:
			self.next = photos[self.index + 1]
			self.last = photos[len(photo_ids) - 1]

		self.count = len(photos)
		self.photo = photos[self.index]

