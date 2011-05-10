import os
import shutil
import tempfile
import types
import time
import mimetypes
import datetime
import zipfile
from logging import info

from pylons import url, request, tmpl_context as c
from pylons.controllers.util import abort, redirect
from pylons.decorators.secure import authenticate_form
from webhelpers.html.tags import link_to

from gallery.lib.base import BaseController, render
from gallery.model import Photo, Album
from gallery.model.meta import Session as s

from gallery.lib import utils
from gallery.lib.utils import *

def add_archive(aid, file, arc_type):
	"""
	Add archive with photos to a given album
	"""

	print "extracting archive ..."
	z = zipfile.ZipFile(file)
	for fname in z.namelist():
		if mimetypes.guess_type(fname)[0] == "image/jpeg":
			photo = Photo(os.path.basename(fname), aid, z.read(fname))
			s.add(photo)
			s.commit()

class AdminController(BaseController):

	requires_auth = True

	def index(self):
		# Return a rendered template
		#   return render('/some/template.mako')
		# or, Return a response
		return render("/admin.mako")

	def photo_add(self, aid):
			return render("/photo_add.mako")

	def photo_add_single(self, aid, new_photo):
		name = new_photo.filename.lstrip(os.sep)

		tp = mimetypes.guess_type(name)[0]

		if tp == "image/jpeg":
			photo = Photo(name, aid, new_photo.file.read())
			new_photo.file.close()
			s.add(photo)
			s.commit()
		elif tp == "application/zip":
			add_archive(aid, new_photo.file, arc_type = "zip")
		else:
			return "Unsupported type"
		return None

	@authenticate_form
	def photo_add_submit(self, aid):
		for i in range(20):
			new_photo = request.params.get('new_photo-%d' % i)
			if type(new_photo) is not types.InstanceType:
				continue
			s = self.photo_add_single(aid, new_photo)
			if s:
				return s

		redirect(url(controller = "album",
					action = "show_first_page", aid = aid))
			
	def photo_del_submit(self, aid, pid):
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
		c.photo = s.query(Photo).filter_by(album_id=aid, id=pid)[0]
		
		return render('/photo_edit.mako')

	@authenticate_form
	def photo_edit_submit(self, aid, pid):
		if request.params.get("Cancel"):
			redirect(url(controller="album",
						action = "show_first_page", aid = aid))

		photo = s.query(Photo).filter_by(album_id=aid, id=pid)[0]

		photo.display_name = request.params.get("title")
		photo.hidden = bool(request.params.get("hide_photo", 0))

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

		c.album = s.query(Album).filter(Album.id == aid).first()
		if not c.album:
			abort(404)

		return render('album_edit.mako')

	@authenticate_form
	def album_edit_submit(self, aid):
		if request.params.get("Cancel"):
			redirect(url(controller="album"))

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
			old_preview = album.preview

			# add preview
			name = new_thumb.filename.lstrip(os.sep)
			preview = Photo(name, aid, new_thumb.file.read())
			new_thumb.file.close()
			preview.hidden = True
			s.add(preview)
			s.commit()

			album.preview_id = preview.id
			if old_preview:
				s.delete(old_preview)

		s.commit()

		redirect(url(controller = "album",
				action = "show_first_page", aid = aid))

	def album_del(self, aid):
		album = s.query(Album).filter(Album.id == aid).first()
		if not album:
			abort(404)

		s.delete(album)
		s.commit()

		redirect(url(controller = "album",
					action = "show_first_page", aid = album.parent_id))

