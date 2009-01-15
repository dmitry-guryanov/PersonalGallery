import logging

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa


from gallery.lib import utils

log = logging.getLogger(__name__)

class AlbumController(BaseController):

	def index(self):
		return self.show_page('0', '0')

	def show_first_page(self, aid):
		return self.show_page(aid, '0')

	def show_page(self, aid, page):
		c.album = aid
		c.page = page
		c.u = utils

		s = meta.Session

		# top albums
		c.top_albums = s.query(Album).filter(Album.parent_id == 0).filter(Album.id != 0).all()

		cur_album = s.query(Album).filter(Album.id == aid).all()[0]
		c.cur_album = cur_album

		albums_q = s.query(Album).filter(Album.parent_id == aid)
		albums = albums_q.all()
		c.albums = albums

		photos_q = s.query(Photo).filter(Photo.album_id == aid)
		photos = photos_q.all()
		c.photos = photos



		if 'user' in session:
			c.admin = True

		s.close()
		return render("/album.mako")
