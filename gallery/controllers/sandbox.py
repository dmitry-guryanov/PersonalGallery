import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from gallery.lib.base import BaseController, render

log = logging.getLogger(__name__)

class SandboxController(BaseController):

	def index(self):
		# Return a rendered template
		#return render('/sandbox.mako')
		# or, return a string
		return render("/sandbox.mako")

	def req(self):
		return "<qwe>xxx</qwe>"
