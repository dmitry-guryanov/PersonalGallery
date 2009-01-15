import logging
import os
import shutil
from commands import *

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

def get_photo_path(aid, pid):
#	stpath = config['pylons.paths']['static_files']
	return os.path.join(permanent_store, str(aid),
									str(pid) + ".jpg")

def get_preview_path(aid, pid):
#	stpath = config['pylons.paths']['static_files']
	return os.path.join(permanent_store, str(aid),
									"previews", str(pid) + ".jpg")

def get_web_photo_path(aid, pid):
	return "%s/%s/%s.jpg" % (web_static_path, str(aid), str(pid))

def get_web_preview_path(aid, pid):
	return "%s/%s/previews/%s.jpg" % (web_static_path, str(aid), str(pid))

def _get_image_info(path):
	out = getoutput("identify \"%s\"" % path).strip()
	
	img = Image()
	
	size = out.split()[2]
	i = size.index('x')
	img.width = int(size[:i])
	img.height = int(size[i + 1:])
	return img

def get_photo_info(album, photo):
	return _get_image_info(get_photo_path(album, photo))

