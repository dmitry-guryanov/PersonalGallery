from pyramid.config import Configurator
from pyramid.events import NewRequest, BeforeRender
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from gallery.models import appmaker

def main(global_config, **settings):
	""" This function returns a WSGI application.
	"""
	engine = engine_from_config(settings, 'sqlalchemy.')
	get_root = appmaker(engine, **settings)
	authentication_policy = AuthTktAuthenticationPolicy('seekrit')
	authorization_policy = ACLAuthorizationPolicy()

	config = Configurator(settings = settings, root_factory = get_root,
			authentication_policy = authentication_policy,
			authorization_policy = authorization_policy)

	config.add_static_view('static', 'gallery:static')
	config.scan('gallery.views')

	config.add_subscriber("gallery.subscribers.new_request", NewRequest)
	config.add_subscriber("gallery.subscribers.before_render", BeforeRender)

	return config.make_wsgi_app()

