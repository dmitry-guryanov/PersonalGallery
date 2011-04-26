from logging import info

from pylons import tmpl_context as c
from gallery.model import meta, Photo, Album

def setup_header():
	s = meta.Session

	# top albums
	c.top_albums = s.query(Album).filter(Album.parent_id == 0).filter(Album.id != 0).all()
