"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import session

from gallery.model import meta

class BaseController(WSGIController):
    requires_auth = False

    def __before__(self):
        # Authentication required?
        if self.requires_auth and 'user' not in session:
            # Remember where we came from so that the user can be sent there
            # after a successful login
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(h.url_for(controller='login'))

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()

