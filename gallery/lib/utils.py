import logging
import os
import shutil
from commands import *
import re

from gallery.lib.base import *
from gallery.model import meta, Photo, Album
import sqlalchemy as sa

from pylons import config

log = logging.getLogger(__name__)

permanent_store = "/home/dimak/gallery-static/photos"
web_static_path = "/gallery-static/photos"


preview_size = 150

class Image:
	width = 0
	height = 0

def get_photo_path(photo):
#	stpath = config['pylons.paths']['static_files']
	return os.path.join(permanent_store, str(photo.album_id), photo.name)

def get_preview_path(photo):
#	stpath = config['pylons.paths']['static_files']
	preview_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", photo.name)
	return os.path.join(permanent_store, str(photo.album_id),
								"previews", preview_name)

def get_album_path(album):
	return os.path.join(permanent_store, str(album.id))

def get_album_preview_path(album):
	return os.path.join(permanent_store, str(album.id), "previews")

def get_web_album_thumb(album):
	return "%s/%s/previews/%s" % (web_static_path, album.id, "000-album-preview-preview.jpg")

def get_web_photo_path(photo):
	return "%s/%s/%s" % (web_static_path, str(photo.album_id), photo.name)

def get_web_preview_path(photo):
	preview_name = re.sub("([^\.]+)\..+", r"\1-preview.jpg", photo.name)
	return "%s/%s/previews/%s" % (web_static_path,
							str(photo.album_id), preview_name)

def _get_image_info(path):
	out = getoutput("identify \"%s\"" % path).strip()
	
	img = Image()
	
	size = out.split()[2]
	i = size.index('x')
	img.width = int(size[:i])
	img.height = int(size[i + 1:])
	return img

def get_photo_info(photo):
	return _get_image_info(get_photo_path(photo))

