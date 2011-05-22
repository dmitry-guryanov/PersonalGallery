## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%def name="header()">
<%include file="header.mako"/>
</%def>
% if c.photos:
	<div class="gallery-thumbs">
	<% i = 1 %>
% for p in c.photos:
		<h3 style="text-align: left; padding-left: 10px;">${i}.</h3>
		<div class="gallery-thumbs2">
			<img alt="${p.display_name}" src="${p.get_web_path()}"/>
		</div>
	<% i += 1 %>
% endfor
		<div style="clear: both"></div>
	</div>
% else:
	<h2>There are no photos in this album</h2>
% endif

