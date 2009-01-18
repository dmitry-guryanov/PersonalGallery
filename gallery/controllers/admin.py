import logging
import os
import shutil
import tempfile
import types
import mimetypes

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa

from pylons import config

from gallery.lib.utils import *

log = logging.getLogger(__name__)

def resolve_dup_name(path):
	dirname, filename = os.path.split(path)
	name, ext = os.path.splitext(filename)

	i = 1
	while 1:
		new_name = "%s--%.3d%s" % (name, i, ext)
		new_path = os.path.join(dirname, new_name)
		if not os.access(new_path, os.F_OK):
			return (new_name, new_path)
		i += 1

def add_photo(aid, name, file):
	"""
	Add single photo to album with given ID
	"""

	ph = Photo()
	ph.name = name
	ph.path = name
	ph.album_id = aid

	s = meta.Session

	# save file
	photo_path = get_photo_path(ph)
	if os.access(photo_path, os.F_OK):
		ph.name, photo_path = resolve_dup_name(photo_path)

	shutil.copyfile(file, photo_path)

	# make preview
	inf = get_photo_info(ph)
	preview_file = get_preview_path(ph)

	if inf.width > inf.height:
		crop_cmd = "%dx%d+%d+0" % (inf.height, inf.height, (inf.width - inf.height) / 2)
	else:
		crop_cmd = "%dx%d+0+%d" % (inf.width, inf.width, (inf.height - inf.width) / 8)

	cmd = "convert %s -crop %s -resize %d %s" % (photo_path, crop_cmd,
								preview_size, preview_file)
	os.system(cmd)

	ph.width = inf.width
	ph.height = inf.height
	s.save(ph)
	s.commit()

def add_archive(aid, file, arc_type):
	"""
	Add archive with photos to a given album
	"""

	print "extracting archive ..."

	tmpdir = tempfile.mkdtemp()

	os.system("unzip %s -d %s" % (file, tmpdir))

	for root, dirs, files in os.walk(tmpdir):
		for f in files:
			fpath = os.path.join(root, f)
			tp = mimetypes.guess_type(fpath)[0]
			if tp == "image/jpeg":
				add_photo(aid, f, fpath)
	
	shutil.rmtree(tmpdir)

class AdminController(BaseController):

	requires_auth = True

	def index(self):
		# Return a rendered template
		#   return render('/some/template.mako')
		# or, Return a response
		return render("/admin.mako")

	def photo_add(self, aid):
			return render("/photo_add.mako")

	def photo_add_submit(self, aid):

			for i in range(20):
				new_photo = request.params.get('new_photo-%d' % i)
				if type(new_photo) is not types.InstanceType:
					continue

				name = new_photo.filename.lstrip(os.sep)
				(tmpfd, tmpname) = tempfile.mkstemp(suffix=name)
				tmpobj = os.fdopen(tmpfd, "w")
				shutil.copyfileobj(new_photo.file, tmpobj)
				tmpobj.close()
				new_photo.file.close()

				mimetypes.init()

				tp = mimetypes.guess_type(tmpname)[0]

				if tp == "image/jpeg":
					add_photo(aid, name, tmpname)
				elif tp == "application/zip":
					add_archive(aid, tmpname, arc_type = "zip")
				else:
					os.unlink(tmpname)
					return "Unsupported type"

				os.unlink(tmpname)

			h.redirect_to(controller = "/album", action = "show_first_page", aid = aid)
			
	def photo_del_submit(self, aid, pid):

			s = meta.Session

			photo_q = s.query(Photo)
			photos = photo_q.filter_by(album_id=aid, id=pid).all()
			photo_obj = photos[0]

			msg = "<pre>"

			try:
				os.unlink(get_photo_path(photo_obj))
			except Exception, e:
				msg += str(e) + "\n"

			try:
				os.unlink(get_preview_path(photo_obj))
			except Exception, e:
				msg += str(e) + "\n"
			msg += "</pre>"

			s.delete(photo_obj)
			s.commit()

			h.redirect_to(controller = "/album", action = "show_first_page", aid = aid)

	def album_edit(self, aid):
		c.aid = aid

		s = meta.Session

		albums_q = s.query(Album).filter(Album.id == aid)
		albums = albums_q.all()
		c.album = albums[0]

		return render('/album_edit.mako')

	def album_edit_submit(self, aid):
		if request.params.get("Cancel"):
			h.redirect_to(controller="/album")

		s = meta.Session

		albums_q = s.query(Album).filter(Album.id == aid)
		albums = albums_q.all()
		album = albums[0]

		album.name = request.params.get("name")
		album.display_name = request.params.get("title")
		album.descr = request.params.get("description")

		s.commit()

		h.redirect_to(controller = "/album", action = "show_first_page", aid = aid)

