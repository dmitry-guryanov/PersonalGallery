import logging

from gallery.lib.base import *

log = logging.getLogger(__name__)

class HelloController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'

    def serverinfo(self):
        import cgi
        import pprint
        c.pretty_environ = cgi.escape(pprint.pformat(request.environ))
        c.name = 'The Black Knight'
        return render('/serverinfo.mako')
