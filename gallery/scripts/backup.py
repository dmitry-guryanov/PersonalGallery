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


def backup_album(d, s, a):
	pd = os.mkdir(os.path.join(d, "previews"))

	adict = {}
	adict["id"] = a.id
	adict["display_name"] = a.display_name
	adict["created"] = a.created
	adict["preview_id"] = a.preview_id
	adict["descr"] = a.descr
	adict["hidden"] = a.hidden
	adict["sort_by"] = a.sort_by

	l = []
	for p in a.photos:
		pdict = {}
		pdict["id"] = p.id
		pdict["name"] = p.name
		pdict["display_name"] = p.display_name
		pdict["created"] = p.created
		pdict["width"] = p.width
		pdict["height"] = p.height
		pdict["hidden"] = p.hidden
		l.append(pdict)

		photo_name = os.path.basename(p.get_path())
		preview_name = os.path.basename(p.get_preview_path())
		shutil.copy(p.get_path(), os.path.join(d, photo_name))
		shutil.copy(p.get_preview_path(),
			os.path.join(d, "previews", preview_name))

	adict["photos"] = l

	f = open(os.path.join(d, "info.yaml"), "w")
	yaml.dump(adict, f)
	f.close()

	for album in a.albums:
		d2 = os.path.join(d, "album-%d" % album.id)
		os.mkdir(d2)
		backup_album(d2, s, album)

def main():
	if len(sys.argv) != 3:
		sys.exit("Usage: python -m test4.scripts.create_db INI_FILE OUT_FILE")
	ini_file = sys.argv[1]
	out_path = sys.argv[2]

	if os.path.exists(out_path):
		raise Exception("%s already exists" % out_path)

	logging.config.fileConfig(ini_file)
	log = logging.getLogger(__name__)
	app = get_app(ini_file, "PersonalGallery")
	settings = app.registry.settings

	config.config = settings

	s = models.DBSession()

	if not out_path.endswith(".tar.bz2"):
		raise Exception("Only .tar.bz2 archives supported")

	out_name = os.path.basename(out_path)
	out_name = out_name[:-len(".tar.bz2")]

	tmpdir = tempfile.mkdtemp()
	try:
		q = s.query(Album).filter_by(id = 1)
		a = q.one()
		backup_album(tmpdir, s, a)

		t = tarfile.open(out_path, "w:bz2")
		t.add(tmpdir, out_name, recursive = True)
		t.close()
	finally:
		shutil.rmtree(tmpdir)

if __name__ == "__main__":  
	main()
