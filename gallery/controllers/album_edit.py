import logging

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa

log = logging.getLogger(__name__)

class AlbumEditController(BaseController):

	def index(self, album):
		c.album = album

		s = meta.Session

		albums_q = s.query(Album).filter(Album.parent_id == album)
		albums = albums_q.all()
		c.albums = albums

		photos_q = s.query(Photo).filter(Photo.album_id == album)
		photos = photos_q.all()
		c.photos = photos
		return render('/album_edit.mako')

