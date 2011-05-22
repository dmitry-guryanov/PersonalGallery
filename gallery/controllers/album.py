from logging import info

from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons import config, url

from webhelpers.paginate import Page

from gallery.lib.base import BaseController, render
from gallery.model import Photo, Album
from gallery.model.meta import Session as s

from gallery.lib import utils

class AlbumController(BaseController):

	def index(self):
		return self.show_first_page(config["root_album_id"])

	def show_first_page(self, aid):
		return self.show_page(aid, 0)

	def show_photos(self, aid):
		return self.show_page(aid, 0, True)

	def show_page(self, aid, page, show_photos = False):
		c.page = page
		c.u = utils

		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		c.albums = self._get_albums(aid, page)
		c.photos = self._get_photos(aid, page)

		c.counts = self._get_counts(c.album)

		if show_photos:
			return render("/photo-all.mako")
		else:
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
			return url(controller = "album", action = "show_page", aid = aid, page = page)
					
		return Page(albums_q, page = page, items_per_page = 8, url = _get_page_url)

	def _get_photos(self, aid, page):
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
			return url(controller = "album", action = "show_page", aid = aid, page = page)
					
		return Page(photos_q, page = page, items_per_page = 20, url = _get_page_url)

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

