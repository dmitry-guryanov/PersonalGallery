import logging
import os
import shutil
import tempfile
import types
import time
import mimetypes
import datetime

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from gallery.lib.base import BaseController, render
from pylons import url
from gallery.lib.helpers import link_to
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

def add_photo(aid, name, file, photo = None, only_file = False, rewrite = False):
	"""
	Add single photo to album with given ID
	"""

	if not photo:
		ph = Photo()
	else:
		ph = photo
	ph.name = unicode(name)
	ph.album_id = aid

	s = meta.Session

	# save file
	photo_path = get_photo_path(ph)
	if os.access(photo_path, os.F_OK):
		if rewrite:
			os.unlink(photo_path)
			os.unlink(get_preview_path(ph))
		else:
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

	if not only_file:
		ph.width = inf.width
		ph.height = inf.height
		if inf.exif.has_key("Create Date"):
			str_date = inf.exif["Create Date"]
			if re.match("\d+:\d+:\d+ \d+:\d+:\d+.\d+", str_date):
				str_date = str_date[:-3]
			cr_time = time.strptime(str_date, "%Y:%m:%d %H:%M:%S")
			cr_ts = time.mktime(cr_time)
			ph.created = datetime.datetime.fromtimestamp(cr_ts)
		else:
			ph.created = datetime.datetime.now()
		
		if not photo:
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

def del_photo(photo):
	s = meta.Session

	msg = ""
	try:
		os.unlink(get_photo_path(photo))
	except OSError, e:
		msg += str(e) + "\n"

	try:
		os.unlink(get_preview_path(photo))
	except OSError, e:
		msg += str(e) + "\n"

	s.delete(photo)
	s.commit()
	return msg

def del_album(album):

	s = meta.Session

	child_albums = s.query(Album).filter(Album.parent_id == album.id).all()

	msg = ""

	for a in child_albums:
		msg += del_album(a)

	photos = s.query(Photo).filter(Photo.album_id == album.id).all()

	for p in photos:
		msg += del_photo(p)

	s.delete(album)

	try:
		shutil.rmtree(get_album_path(album))
	except OSError, e:
		msg += str(e) + "\n"

	s.commit()

	return msg

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

			redirect_to(controller = "/album",
						action = "show_first_page", aid = aid)
			
	def photo_del_submit(self, aid, pid):

		s = meta.Session

		photo_q = s.query(Photo)
		photos = photo_q.filter_by(album_id=aid, id=pid).all()
		photo_obj = photos[0]

		msg = del_photo(photo_obj)

		if msg:
			msg = "<pre>" + msg + "</pre>"
			return msg + link_to("back to album",
				url(controller = "/album",
						action = "show_first_page", aid = aid))
		else:
			redirect_to(controller = "/album",
						action = "show_first_page", aid = aid)

	def photo_edit(self, aid, pid):
		s = meta.Session
		c.photo = s.query(Photo).filter_by(album_id=aid, id=pid)[0]
		
		return render('/photo_edit.mako')

	def photo_edit_submit(self, aid, pid):
		if request.params.get("Cancel"):
			redirect_to(controller="/album",
						action = "show_first_page", aid = aid)

		s = meta.Session

		photo = s.query(Photo).filter_by(album_id=aid, id=pid)[0]

		photo.name = request.params.get("name")
		photo.display_name = request.params.get("title")
		photo.hidden = int(request.params.get("hide_album", 0)) * 65535

		new_photo = request.params.get('photo_file')

		if type(new_photo) is types.InstanceType:
			name = new_photo.filename.lstrip(os.sep)
			(tmpfd, tmpname) = tempfile.mkstemp(suffix=name)
			tmpobj = os.fdopen(tmpfd, "w")
			shutil.copyfileobj(new_photo.file, tmpobj)
			tmpobj.close()
			new_photo.file.close()

			add_photo(aid, name, tmpname, photo = photo,
							only_file = False, rewrite = True)
			photo.name = name
			os.unlink(tmpname)

		s.commit()

		redirect_to(controller="/album",
					action = "show_first_page", aid = aid)

	def album_add(self, aid):
		c.new_album = True
		c.album = Album()
		return render('/album_edit.mako')

	def album_edit(self, aid):
		c.aid = aid
		c.new_album = False

		s = meta.Session

		albums_q = s.query(Album).filter(Album.id == aid)
		albums = albums_q.all()
		c.album = albums[0]

		return render('/album_edit.mako')

	def album_edit_submit(self, aid):
		if request.params.get("Cancel"):
			redirect_to(controller="/album")

		s = meta.Session

		if request.params.get("new_album"):
			album = Album()
			album.parent_id = aid
			s.save(album)
			s.commit()

			os.mkdir(get_album_path(album))
			os.mkdir(get_album_preview_path(album))
		else:
			albums_q = s.query(Album).filter(Album.id == aid)
			albums = albums_q.all()
			album = albums[0]

		album.name = request.params.get("name")
		album.display_name = request.params.get("title")
		album.descr = request.params.get("description")
		album.hidden = int(request.params.get("hide_album", 0)) * 65535

		new_thumb = request.params.get('album_thumbnail')
		print new_thumb, repr(new_thumb)
		if type(new_thumb) is types.InstanceType:
			name = new_thumb.filename.lstrip(os.sep)
			(tmpfd, tmpname) = tempfile.mkstemp(suffix=name)
			tmpobj = os.fdopen(tmpfd, "w")
			shutil.copyfileobj(new_thumb.file, tmpobj)
			tmpobj.close()
			new_thumb.file.close()

			add_photo(album.id, "000-album-preview.jpg", tmpname,
							photo = None, only_file = True, rewrite = True)
			os.unlink(tmpname)

		s.commit()

		redirect_to(controller = "/album",
				action = "show_first_page", aid = aid)

	def album_del(self, aid):
		
		s = meta.Session

		albums_q = s.query(Album).filter(Album.id == aid)
		albums = albums_q.all()
		album = albums[0]

		parent_id = album.parent_id

		msg = del_album(album)

		if msg:
			msg = "<pre>" + msg + "</pre>"
			return msg + link_to("back to album",
				url(controller = "/album",
						action = "show_first_page", aid = parent_id))
		else:
			redirect_to(controller = "/album",
						action = "show_first_page", aid = parent_id)

