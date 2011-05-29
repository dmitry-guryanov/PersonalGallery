## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%def name="head()">
</%def>
<%def name="header()">
<%include file="header.mako"/>
</%def>

	<a href="${url(album)}">back</a>

	<div class="pager">${photos.pager()}</div>
% if photos:
	<div class="gallery-thumbs">
	<% i = photos.first_item %>
% for p in photos:
		<h3 style="text-align: left; padding-left: 10px;">${i}.</h3>
		<div class="photoall-photo">
			<img alt="${p.display_name}" src="${p.get_web_path()}"/>
		</div>
	<% i += 1 %>
% endfor
		<div style="clear: both"></div>
	</div>
	<div class="pager">${photos.pager()}</div>
% else:
	<h2>There are no photos in this album</h2>
% endif

