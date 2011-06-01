"""Create the application's database.

Run this once after installing the application::

	python -m gallery.scripts.create_db development.ini
"""
import logging.config
import os, sys
import shutil
import tarfile
import tempfile

import yaml

from pyramid.paster import get_app

from gallery.lib import config
import gallery.models as models
from gallery.models import Album, Photo


def restore_album(d, s):
	adict = yaml.load(open(os.path.join(d, "info.yaml")))

	a = Album()

	a.id = adict["id"]
	a.display_name = adict["display_name"]
	a.created = adict["created"]
	a.preview_id = adict["preview_id"]
	a.descr = adict["descr"]
	a.hidden = adict["hidden"]
	a.sort_by = adict["sort_by"]
	s.add(a)
	s.commit()

	for pdict in adict["photos"]:
		pfile = pdict["name"]
		if pfile in ["previews", "info.yaml"]:
			continue
		ppath = os.path.join(d, pfile)
		if os.path.isdir(ppath):
			continue

		p = Photo()
		p.id = pdict["id"]
		p.album_id = a.id
		p.name = pdict["name"]
		p.display_name = pdict["display_name"]
		p.created = pdict["created"]
		p.width = pdict["width"]
		p.height = pdict["height"]
		p.hidden = pdict["hidden"]

		photo_name = os.path.basename(p.get_path())
		preview_name = os.path.basename(p.get_preview_path())

		shutil.copy(os.path.join(d, photo_name), p.get_path())
		shutil.copy(os.path.join(d, "previews", preview_name),
					p.get_preview_path())
		s.add(p)

	for afile in os.listdir(d):
		if afile == "previews":
			continue
		apath = os.path.join(d, afile)
		if not os.path.isdir(apath):
			continue

		restore_album(apath, s)

def main():
	if len(sys.argv) != 3:
		sys.exit("Usage: python -m test4.scripts.create_db INI_FILE IN_FILE")
	ini_file = sys.argv[1]
	in_path = sys.argv[2]

	if not os.path.exists(in_path):
		raise Exception("%s doesn't exist" % in_path)

	logging.config.fileConfig(ini_file)
	log = logging.getLogger(__name__)
	app = get_app(ini_file, "PersonalGallery")
	settings = app.registry.settings
	config.config = settings

	s = models.DBSession()

	# Abort if any tables exist to prevent accidental overwriting
	for table in models.Base.metadata.sorted_tables:
		log.debug("checking if table '%s' exists", table.name)
		if table.exists():
			raise RuntimeError("database table '%s' exists" % table.name)

	# Create the tables
	models.Base.metadata.create_all()
	s = models.DBSession()
	s.commit()

	# Put data from backup to gallery
	if not in_path.endswith(".tar.bz2"):
		raise Exception("Only .tar.bz2 archives supported")

	tmpdir = tempfile.mkdtemp()
	print tmpdir
	try:
		t = tarfile.open(in_path, "r:bz2")
		t.extractall(path = tmpdir)
		t.close()

		dirs = os.listdir(tmpdir)
		restore_album(os.path.join(tmpdir, dirs[0]), s)
		s.commit()
	finally:
		shutil.rmtree(tmpdir)

if __name__ == "__main__":  
	main()
