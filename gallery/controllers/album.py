from logging import info

from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons import config

from gallery.lib.base import BaseController, render
from gallery.model import Photo, Album
from gallery.model.meta import Session as s

from gallery.lib import utils

class AlbumController(BaseController):

	def index(self):
		return self.show_first_page(config["root_album_id"])

	def show_first_page(self, aid):
		return self.show_page(aid, 0)

	def show_page(self, aid, page):
		c.album = aid
		c.page = page
		c.u = utils

		c.cur_album = s.query(Album).filter(Album.id == aid).first()
		if not c.cur_album:
			abort(404)

		c.photos = c.cur_album.photos
		if c.cur_album.sort_by == utils.SORT_BY_DATE_DESC:
			c.photos.reverse()

		# get photo counts
		photo_counts = s.execute("SELECT albums.id AS aid, COUNT(*) FROM albums JOIN "
					"photos ON album_id=albums.id "
					"WHERE albums.parent_id=%d GROUP BY photos.album_id;" % int(aid)).fetchall()
		photo_counts = dict(photo_counts)

		# get album counts
		album_counts = s.execute("SELECT albums1.id AS aid, COUNT(*) AS count "
						"FROM albums albums1 JOIN albums albums2 ON "
						"albums2.parent_id=albums1.id "
						"WHERE albums1.parent_id=%d and (albums2.hidden=0 or %d) "
						"GROUP BY albums2.parent_id;" % (int(aid), int(c.admin))).fetchall()
		album_counts = dict(album_counts)

		c.counts = {}
		for a in c.cur_album.albums:
			c.counts[a.id] = (album_counts.get(a.id, 0), photo_counts.get(a.id, 0))

		return render("/album.mako")
