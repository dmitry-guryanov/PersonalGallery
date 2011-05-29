import os
import time
import datetime

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from gallery.models import Article, ArticleRoot, DBSession, get_root

def r(s):
	return "gallery:templates/" + s

@view_config(context = Article, renderer = r("article.mako"))
def view(article, req):
	return dict(article = article)

@view_config(context = ArticleRoot, name = "new",
		renderer = r("article-edit.mako"), permission = "edit")
def new(article, req):
	return dict(article = Article(), new_article = True)

@view_config(context = Article, name = "edit",
		renderer = r("article-edit.mako"), permission = "edit")
def edit(article, req):
	return dict(article = article, new_article = False)

@view_config(context = ArticleRoot, name = "commitnew",
		request_method = "POST", permission = "edit")
@view_config(context = Article, name = "commitedit",
		request_method = "POST", permission = "edit")
def commitedit(context, req):
	s = DBSession()

	if not req.params.get("commit"):
		return HTTPFound(location = req.resource_url(get_root()))

	if req.params.get("new_article"):
		a = Article()
		s.add(a)
	else:
		a = context
	a.title = req.params.get("title", "")
	a.body = req.params.get("body", "")
	s.commit()

	return HTTPFound(location = req.resource_url(a))

@view_config(context = Article, name = "commitdel", permission = "edit")
def commitdel(article, req):
	s = DBSession()

	s.delete(article)
	s.commit()

	return HTTPFound(location = req.resource_url(get_root()))

