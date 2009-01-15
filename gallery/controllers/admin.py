import logging
import os
import shutil
import tempfile
import mimetypes

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa

from pylons import config

from gallery.lib.utils import *

log = logging.getLogger(__name__)


def add_photo(aid, name, file):

	ph = Photo()
	ph.name = name
	ph.path = name
	ph.album_id = aid

	s = meta.Session
	s.save(ph)
	s.commit()

	# save file
	permanent_file_path = get_photo_path(aid, ph.id)
	shutil.copyfile(file, permanent_file_path)

	# make preview
	inf = get_photo_info(aid, ph.id)
	preview_file = get_preview_path(aid, ph.id)

	if inf.width > inf.height:
		crop_cmd = "%dx%d+%d+0" % (inf.height, inf.height, (inf.width - inf.height) / 2)
	else:
		crop_cmd = "%dx%d+0+%d" % (inf.width, inf.width, (inf.height - inf.width) / 8)

	cmd = "convert %s -crop %s -resize %d %s" % (permanent_file_path, crop_cmd,
								preview_size, preview_file)

	ph.width = inf.width
	ph.height = inf.height
	s.commit()

	os.system(cmd)

def add_archive(aid, file, arc_type):

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
			new_photo = request.POST['new_photo']
			
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

			return 'Successfully uploaded: %s, description: %s<br/> <a href="/album/%s">return to album</a>' % \
				(new_photo.filename, request.POST['description'], aid)

	def photo_del_submit(self, aid, pid):

			s = meta.Session

			photo_q = s.query(Photo)
			photos = photo_q.filter_by(album_id=aid, id=pid).all()
			photo_obj = photos[0]

			msg = "<pre>"

			try:
				os.unlink(get_photo_path(aid, pid))
			except Exception, e:
				msg += str(e) + "\n"

			try:
				os.unlink(get_preview_path(aid, pid))
			except Exception, e:
				msg += str(e) + "\n"
			msg += "</pre>"

			s.delete(photo_obj)
			s.commit()

			msg += 'Successfully succesfully deleted <br/> <a href="/album/%s">return to album</a>' % ( aid)

			return msg
		

	def album_edit(self, album):
		c.album = album

		s = meta.Session

		albums_q = s.query(Album).filter(Album.parent_id == album)
		albums = albums_q.all()
		c.albums = albums

		photos_q = s.query(Photo).filter(Photo.album_id == album)
		photos = photos_q.all()
		c.photos = photos
		return render('/album_edit.mako')

