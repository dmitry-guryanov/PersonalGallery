import os
import shutil
import tempfile
import types
import time
import mimetypes
import datetime
from logging import info

from pylons import url, request, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form
from webhelpers.html.tags import link_to

from gallery.lib.base import BaseController, render
from gallery.model import meta, Photo, Album

from gallery.lib import utils
from gallery.lib.utils import *

def add_archive(aid, file, arc_type):
	"""
	Add archive with photos to a given album
	"""

	print "extracting archive ..."
	s = meta.Session

	tmpdir = tempfile.mkdtemp()

	os.system("unzip %s -d %s" % (file, tmpdir))

	for root, dirs, files in os.walk(tmpdir):
		for f in files:
			fpath = os.path.join(root, f)
			tp = mimetypes.guess_type(fpath)[0]
			if tp == "image/jpeg":
				photo = Photo(f, aid, fpath)
				s.add(photo)
				s.commit()
	
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

	@authenticate_form
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
					photo = Photo(name, aid, tmpname)
					s = meta.Session
					s.add(photo)
					s.commit()
				elif tp == "application/zip":
					add_archive(aid, tmpname, arc_type = "zip")
				else:
					os.unlink(tmpname)
					return "Unsupported type"

				os.unlink(tmpname)

			redirect(url(controller = "album",
						action = "show_first_page", aid = aid))
			
	def photo_del_submit(self, aid, pid):

		s = meta.Session

		photo_q = s.query(Photo)
		photo_obj = photo_q.filter_by(album_id=aid, id=pid).first()
		if photo_obj is None:
			c.name = pid
			return render('/photo_not_found.mako')

		s.delete(photo_obj)
		s.commit()

		redirect(url(controller = "album",
					action = "show_first_page", aid = aid))

	def photo_edit(self, aid, pid):
		s = meta.Session
		c.photo = s.query(Photo).filter_by(album_id=aid, id=pid)[0]
		
		return render('/photo_edit.mako')

	@authenticate_form
	def photo_edit_submit(self, aid, pid):
		if request.params.get("Cancel"):
			redirect(url(controller="album",
						action = "show_first_page", aid = aid))

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

#			add_photo(aid, name, tmpname, photo = photo,
#							only_file = False, rewrite = True)
#			photo.name = name

			os.unlink(tmpname)

		s.commit()

		redirect(url(controller="album",
					action = "show_first_page", aid = aid))

	def album_add(self, aid):
		c.u = utils
		c.new_album = True
		c.album = Album()
		return render('album_edit.mako')

	def album_edit(self, aid):
		c.u = utils
		c.aid = aid
		c.new_album = False

		s = meta.Session

		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		return render('album_edit.mako')

	@authenticate_form
	def album_edit_submit(self, aid):
		if request.params.get("Cancel"):
			redirect(url(controller="album"))

		s = meta.Session

		if request.params.get("new_album"):
			album = Album(parent_id = aid)
			s.add(album)
			s.commit()

		else:
			album = s.query(Album).filter(Album.id == aid).first()
			if not album:
				abort(404)

		album.name = request.params.get("name")
		album.display_name = request.params.get("title")
		album.descr = request.params.get("description")
		album.hidden = bool(request.params.get("hide_album", 0))
		album.sort_by = int(request.params.get("sort_by", 1))

		new_thumb = request.params.get('album_thumbnail')
		print new_thumb, repr(new_thumb)
		if type(new_thumb) is types.InstanceType:
			name = new_thumb.filename.lstrip(os.sep)
			(tmpfd, tmpname) = tempfile.mkstemp(suffix=name)
			tmpobj = os.fdopen(tmpfd, "w")
			shutil.copyfileobj(new_thumb.file, tmpobj)
			tmpobj.close()
			new_thumb.file.close()

			# add preview
			preview = Photo(name, album.id, tmpname)
			os.unlink(tmpname)
			s.add(preview)
			s.commit()

			album.preview_id = preview.id

		s.commit()

		redirect(url(controller = "album",
				action = "show_first_page", aid = aid))

	def album_del(self, aid):
		s = meta.Session

		album = s.query(Album).filter(Album.id == aid).first()
		if not album:
			abort(404)

		s.delete(album)
		s.commit()

		redirect(url(controller = "album",
					action = "show_first_page", aid = album.parent_id))

