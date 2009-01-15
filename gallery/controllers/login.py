import logging
import md5

from gallery.lib.base import *

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
		# Both fields filled?
		form_username = str(request.params.get('username'))
		form_password = str(request.params.get('password'))

		if form_username != "dimak":
			return render('/login.mako')

		if md5.md5(password).hexdigest() != md5.md5(form_password).hexdigest():
			return render('/login.mako')

		# Mark user as logged in
		session['user'] = form_username
		session.save()

		# Send user back to the page he originally wanted to get to
		if session.get('path_before_login'):
			redirect_to(session['path_before_login'])
		else: # if previous target is unknown just send the user to a welcome page
			return render('/loggedin.mako')

	def logout(self):
		"""
		Logout the user and display a confirmation message
		"""
		if 'user' in session:
			del session['user']
			session.save()
		return render('/logout.mako')

