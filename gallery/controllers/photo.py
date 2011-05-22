from pylons import tmpl_context as c
from pylons.controllers.util import abort
from pylons.decorators.secure import authenticate_form

from gallery.lib.base import BaseController, render
from gallery.model import Photo, Album
from gallery.model.meta import Session as s
from gallery.lib import utils


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
			first = None
		else:
			prev = photos[cur_idx - 1]
			first = photos[0]

		if cur_idx == len(photo_ids) - 1:
			next = None
			last = None
		else:
			next = photos[cur_idx + 1]
			last = photos[len(photo_ids) - 1]

		return (cur_idx + 1, len(photos), first, prev, next, last)


	def index(self, aid, pid):
		photo_q = s.query(Photo)
		c.photo = photo_q.filter_by(album_id=aid, id=pid).first()

		if c.photo is None:
			abort(404)

		(c.idx, c.all, c.first, c.prev, c.next, c.last) = self._find_adj_photos(s, aid, pid)

		return render('/photo.mako')

