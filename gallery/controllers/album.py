import logging

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa


from gallery.lib import utils

log = logging.getLogger(__name__)

class AlbumController(BaseController):

	def index(self):
		return self.show_first_page(0)

	def show_first_page(self, aid):
		return self.show_page(aid, 0)

	def show_page(self, aid, page):

		if 'user' in session:
			c.admin = True

		c.album = aid
		c.page = page
		c.u = utils

		s = meta.Session

		# top albums
		c.top_albums = s.query(Album).filter(Album.parent_id == 0).filter(Album.id != 0).all()

		cur_album = s.query(Album).filter(Album.id == aid).all()[0]
		c.cur_album = cur_album

		albums_q = s.query(Album).filter(Album.parent_id == aid)
		print dir(albums_q)
		albums = albums_q.all()
		c.albums = albums

		photos_q = s.query(Photo).filter(Photo.album_id == aid).order_by(Photo.id.desc())
		photos = photos_q.all()
		c.photos = photos



		s.close()

		return render("/album.mako")
