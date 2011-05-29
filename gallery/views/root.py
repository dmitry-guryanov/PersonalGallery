from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from gallery.models import MyApp
from gallery.lib.links import get_link

@view_config(context = MyApp)
def view_root(context, req):
	s = req.registry.settings["root_link"]
	return HTTPFound(location = get_link(req, s).url)

