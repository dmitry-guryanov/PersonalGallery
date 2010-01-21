import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from gallery.lib.base import BaseController, render

from gallery.model import meta, Photo, Album
import sqlalchemy as sa

import sys

import types

from gallery.lib import utils

log = logging.getLogger(__name__)



class PhotoController(BaseController):

	def _find_adj_photos(self, s, aid, pid):
		photos_q = s.query(Photo).filter(Photo.album_id == aid)

		cur_album = s.query(Album).filter(Album.id == aid).first()

		if cur_album.sort_by == utils.SORT_BY_DATE:
			photos_q = photos_q.order_by(Photo.created)
		elif cur_album.sort_by == utils.SORT_BY_DATE_DESC:
			photos_q = photos_q.order_by(Photo.created.desc())

		photos = photos_q.all()

		photo_ids = map(lambda x: x.id, photos)
		cur_idx = photo_ids.index(long(pid))

		if cur_idx == 0:
			prev = None
		else:
			prev = photos[cur_idx - 1]

		if cur_idx == len(photo_ids) - 1:
			next = None
		else:
			next = photos[cur_idx + 1]

		return (prev, next)


	def index(self, aid, pid):

		if 'user' in session:
			c.admin = True

		c.u = utils
		s = meta.Session

		photo_q = s.query(Photo)
		c.photo = photo_q.filter_by(album_id=aid, id=pid).first()

		if c.photo is None:
			abort(404)

		(c.prev, c.next) = self._find_adj_photos(s, aid, pid)

		return render('/photo.mako')

