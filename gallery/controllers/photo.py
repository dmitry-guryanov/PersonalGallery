import logging

from gallery.lib.base import *

from gallery.model import meta, Photo, Album
import sqlalchemy as sa

import sys

import types

from gallery.lib import utils

log = logging.getLogger(__name__)



class PhotoController(BaseController):

	def index(self, aid, pid):

		if 'user' in session:
			c.admin = True

		c.u = utils

		s = meta.Session

		photo_q = s.query(Photo)
		photos = photo_q.filter_by(album_id=aid, id=pid).all()

	
		if len(photos) != 1:
			c.name = pid
			return render('/photo_not_found.mako')
		else:
			c.photo = photos[0]

		photos_q = s.query(Photo).filter(Photo.album_id == aid)

		cur_album = s.query(Album).filter(Album.id == aid).all()[0]
		c.cur_album = cur_album

		if cur_album.sort_by == utils.SORT_BY_DATE:
			photos_q = photos_q.order_by(Photo.created)
		elif cur_album.sort_by == utils.SORT_BY_DATE_DESC:
			photos_q = photos_q.order_by(Photo.created.desc())

		photos = photos_q.all()

		photo_ids = map(lambda x: x.id, photos)

		cur_idx = photo_ids.index(c.photo.id)

		if cur_idx == 0:
			c.prev = None
		else:
			c.prev = photos[cur_idx - 1]

		if cur_idx == len(photo_ids) - 1:
			c.next = None
		else:
			c.next = photos[cur_idx + 1]

		return render('/photo.mako')

