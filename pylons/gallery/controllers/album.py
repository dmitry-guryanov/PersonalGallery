from logging import info

from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons import config, url

from webhelpers.paginate import Page

from gallery.lib.base import BaseController, render
from gallery.model import Photo, Album
from gallery.model.meta import Session as s

from gallery.lib import utils

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

class AlbumController(BaseController):

	def index(self):
		return self.show_first_page(config["root_album_id"])

	def show_first_page(self, aid):
		return self.show_page(aid, 0)

	def show_photos(self, aid, page = 0):
		c.u = utils
		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		c.photos = self._get_photos(aid, page, "show_photos", 10)[1]

		return render("/photo-all.mako")

	def show_photo(self, aid, page, pid):
		pid = int(pid)
		c.u = utils
		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		c.albums = self._get_albums(aid, page)
		all_ph, c.photos = self._get_photos(aid, page, "show_page", 16)

		try:
			c.pnav = PhotosNav(all_ph, pid)
		except PhotosNavError:
			abort(404)

		c.photo = c.pnav.photo
		c.counts = self._get_counts(c.album)

		return render("/album.mako")

	def get_photo_ajax(self, aid, pid):
		pid = int(pid)
		c.u = utils

		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		all_ph, c.photos = self._get_photos(aid, 1, "show_page", 16)

		try:
			c.pnav = PhotosNav(all_ph, pid)
		except PhotosNavError:
			abort(404)

		return render("/album-getphoto.mako")

	def show_page(self, aid, page):
		c.u = utils
		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		c.albums = self._get_albums(aid, page)
		c.photos = self._get_photos(aid, page, "show_page", 16)[1]

		c.counts = self._get_counts(c.album)

		return render("/album.mako")

	def _get_albums(self, aid, page):
		"""
		Return Page for albums
		"""
		albums_q = s.query(Album).filter(Album.parent_id == aid)
		# hide albums only for guests
		if not c.admin:
			albums_q = albums_q.filter(Album.hidden == False)

		def _get_page_url(page, partial=None):
			return url(controller = "album", action = "show_page",
							aid = aid, page = page)
					
		return Page(albums_q, page = page,
			items_per_page = 8, url = _get_page_url)

	def _get_photos(self, aid, page, act, items_per_page):
		"""
		Return Page for photos
		"""
		photos_q = s.query(Photo).filter(Photo.album_id == aid)
		# hide photos only for guests
		if not c.admin:
			photos_q = photos_q.filter(Photo.hidden == False)
		if c.album.sort_by == utils.SORT_BY_DATE:
			photos_q = photos_q.order_by(Photo.created)
		elif c.album.sort_by == utils.SORT_BY_DATE_DESC:
			photos_q = photos_q.order_by(Photo.created.desc())

		def _get_page_url(page, partial=None):
			return url(controller = "album", action = act,
						aid = aid, page = page)
		all_photos = photos_q.all()
		return (all_photos, Page(all_photos, page = page,
			items_per_page = items_per_page, url = _get_page_url))

	def _get_counts(self, album):
		# get photo counts
		photo_counts = s.execute("SELECT albums.id AS aid, COUNT(*) FROM albums JOIN "
					"photos ON album_id=albums.id "
					"WHERE albums.parent_id=%d GROUP BY photos.album_id;" % int(album.id)).fetchall()
		photo_counts = dict(photo_counts)

		# get album counts
		album_counts = s.execute("SELECT albums1.id AS aid, COUNT(*) AS count "
						"FROM albums albums1 JOIN albums albums2 ON "
						"albums2.parent_id=albums1.id "
						"WHERE albums1.parent_id=%d and (albums2.hidden=0 or %d) "
						"GROUP BY albums2.parent_id;" % (int(album.id), int(c.admin))).fetchall()
		album_counts = dict(album_counts)

		counts = {}
		for a in c.album.albums:
			counts[a.id] = (album_counts.get(a.id, 0), photo_counts.get(a.id, 0))
		return counts

