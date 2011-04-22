# -*- coding: utf-8 -*-
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

SORT_BY_DATE		= 1
SORT_BY_DATE_DESC	= 2

sorting_names = {
	SORT_BY_DATE: u"по возрастанию времени создания",
	SORT_BY_DATE_DESC: u"по убыванию даты создания"}

preview_size = 150

class Image:
	width = 0
	height = 0

def _get_image_info(path):
	out = getoutput("identify \"%s\"" % path).strip()
	
	img = Image()
	
	size = out.split()[2]
	i = size.index('x')
	img.width = int(size[:i])
	img.height = int(size[i + 1:])
	img.exif = {}

	exif_strs = getoutput("exiftool \"%s\"" % path).splitlines()
	for s in exif_strs:
		tag, value = s.split(":", 1)
		tag = tag.strip()
		value = value.strip()
		img.exif[tag] = value

	return img

def get_photo_info(photo):
	return _get_image_info(photo.get_path())


mult_words = {
	"photo": [u"фотографий", u"фотография", u"фотографии"],
	"album": [u"альбомов", u"альбом", u"альбома"]
}

def get_mult_word(word, n):
	if n >= 10 and n < 20:
		return mult_words[word][0]
	elif n % 10 == 1:
		return mult_words[word][1]
	elif n % 10 >= 2 and n % 10 < 5:
		return mult_words[word][2]
	else:
		return mult_words[word][0]

