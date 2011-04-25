import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort
from pylons import config

from gallery.lib.base import BaseController, render
from pylons import url
from gallery.model import meta, Photo, Album
import sqlalchemy as sa


from gallery.lib import utils

log = logging.getLogger(__name__)

class AlbumController(BaseController):

	def index(self):
		return self.show_first_page(config["root_album_id"])

	def show_first_page(self, aid):
		return self.show_page(aid, 0)

	def show_page(self, aid, page):
		c.album = aid
		c.page = page
		c.u = utils

		s = meta.Session

		c.cur_album = s.query(Album).filter(Album.id == aid).first()
		if not c.cur_album:
			abort(404)

		albums_q = s.query(Album).filter(Album.parent_id == aid)

		# hide albums only for guests
		if not c.admin:
			albums_q = albums_q.filter(Album.hidden != 1)

		albums = albums_q.all()
		c.albums = albums

		photos_q = s.query(Photo).filter(Photo.album_id == aid)
		
		if c.cur_album.sort_by == utils.SORT_BY_DATE:
			photos_q = photos_q.order_by(Photo.created)
		elif c.cur_album.sort_by == utils.SORT_BY_DATE_DESC:
			photos_q = photos_q.order_by(Photo.created.desc())

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
						"GROUP BY albums2.parent_id;" % (int(aid), int('user' in session))).fetchall()
		album_counts = dict(album_counts)

		c.counts = {}
		for a in albums:
			c.counts[a.id] = (album_counts.get(a.id, 0), photo_counts.get(a.id, 0))

		photos = photos_q.all()
		c.photos = photos

		s.close()

		return render("/album.mako")
