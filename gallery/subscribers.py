from pyramid.events import NewRequest, BeforeRender, subscriber
from pyramid.security import authenticated_userid

from gallery.models import get_root
from gallery.lib import helpers

from gallery.lib import config #FIXME
from gallery.lib.links import get_link

@subscriber(NewRequest)
def new_request(event):
	event.request.admin = (authenticated_userid(event.request) == "dimak")
	config.config = event.request.registry.settings

@subscriber(BeforeRender)
def before_render(event):
	top_links = make_top_links(event.get("request"))
	d = {
		"root": get_root(),
		"url": event.get("request").resource_url,
		"h": helpers,
		"admin": authenticated_userid(event.get("request")),
		"top_links": top_links,
	}

	event.update(d)

def make_top_links(req):
	txt = req.registry.settings["top_links"]

	links = []
	lines = txt.strip().splitlines()
	for line in lines:
		links.append(get_link(req, line))
	return links
