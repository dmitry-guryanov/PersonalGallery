## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%def name="header()">
<%include file="header.mako"/>
</%def>

	<a href="${url(controller = 'album', action = 'show_page', aid = c.album.id, page = c.photos.page)}">вернуться к миниатюрам</a>
	<div class="pager">${c.photos.pager()}</div>
% if c.photos:
	<div class="gallery-thumbs">
	<% i = c.photos.first_item %>
% for p in c.photos:
		<h3 style="text-align: left; padding-left: 10px;">${i}.</h3>
		<div class="gallery-thumbs2">
			<a href="${url(controller = 'photo', action = 'index', aid = c.album.id, pid = p.id)}"
			<img alt="${p.display_name}" src="${p.get_web_path()}"/>
			</a>
		</div>
	<% i += 1 %>
% endfor
		<div style="clear: both"></div>
	</div>
	<div class="pager">${c.photos.pager()}</div>
% else:
	<h2>There are no photos in this album</h2>
% endif

