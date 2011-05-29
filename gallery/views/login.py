from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.renderers import get_renderer
from pyramid.security import remember, forget, authenticated_userid
from pyramid.httpexceptions import HTTPFound

from gallery.models import LoginRoot, get_root

def r(s):
	return "gallery:templates/" + s

@view_config(context = LoginRoot, renderer = r("login.mako"))
def view(context, req):
	return dict(admin = 0)

@view_config(context = LoginRoot, name = "login")
def login(context, req):
	if "cancel" in req.params:
		return HTTPFound(location = root_url)

	root_url = req.resource_url(get_root(req))
	login_url = req.resource_url(context)

	form_username = str(req.params.get('username')).lower()
	form_password = str(req.params.get('password'))

	if form_username != "admin":
		return HTTPFound(location = login_url)
	if "qweqwe" != form_password:
		return HTTPFound(location = login_url)

	headers = remember(req, form_username, max_age = '86400')
	response = HTTPFound(location = root_url)
	response.headerlist.extend(headers)
	return response

@view_config(context = LoginRoot, name = "logout")
def logout(context, req):
	headers = forget(req)
	response = HTTPFound(location = req.resource_url(get_root(req)))
	response.headerlist.extend(headers)
	return response

