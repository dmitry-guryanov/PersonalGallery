import logging
import md5

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from gallery.lib.base import BaseController, render

log = logging.getLogger(__name__)

username = "dimak"
password = "qweqwe"

class LoginController(BaseController):
	def index(self):
		"""
		Show login form. Submits to /login/submit
		"""
		return render('/login.mako')

	def submit(self):
		"""
		Verify username and password
		"""

		if request.params.get("Cancel"):
			redirect_to(controller="/album")

		# Both fields filled?
		form_username = str(request.params.get('username')).lower()
		form_password = str(request.params.get('password'))

		if form_username != "dimak":
			return render('/login.mako')

		if md5.md5(password).hexdigest() != md5.md5(form_password).hexdigest():
			return render('/login.mako')

		# Mark user as logged in
		session['user'] = form_username
		session.save()


		redirect_to(controller="/album")

	def logout(self):
		"""
		Logout the user and display a confirmation message
		"""
		if 'user' in session:
			del session['user']
			session.save()
		redirect_to(controller="/album")

