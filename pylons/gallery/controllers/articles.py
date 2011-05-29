import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from gallery.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ArticlesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('article', 'articles')

    def index(self, format='html'):
        """GET /articles: All items in the collection"""
	return "qweqwe"
        # url('articles')

    def create(self):
        """POST /articles: Create a new item"""
        # url('articles')

	return "create"

    def new(self, format='html'):
        """GET /articles/new: Form to create a new item"""
        # url('new_article')
	return render("/article-edit.mako")

    def update(self, id):
        """PUT /articles/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('article', id=ID),
        #           method='put')
        # url('article', id=ID)

    def delete(self, id):
        """DELETE /articles/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('article', id=ID),
        #           method='delete')
        # url('article', id=ID)

    def show(self, id, format='html'):
        """GET /articles/id: Show a specific item"""
	return id
        # url('article', id=ID)

    def edit(self, id, format='html'):
        """GET /articles/id/edit: Form to edit an existing item"""
        # url('edit_article', id=ID)
