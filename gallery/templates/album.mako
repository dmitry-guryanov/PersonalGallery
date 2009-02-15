## -*- coding: utf-8 -*-
<%inherit file="base.html"/>
<%def name="header()">
</%def>

<%include file="header.mako"/>

% if c.albums:
	<div class="gallery-thumbs">
% for a in c.albums:
		<div class="gallery-album">
			<div class="gallery-thumb">
				<a class="gallery-thumb-link" href='${h.url_for(controller="/album", action="show_first_page", aid=a.id)}'>
						<img style="position: relative" alt="${a.display_name}" src="${c.u.get_web_album_thumb(a)}"/>
				</a>
			</div>
			<div class="album-link">
			<a href='${h.url_for(controller="/album", action="show_first_page", aid=a.id)}'>
				${a.display_name}
			</a>
			</div>
			<span class="meta">
			${len(a.photos)} фотографий<br/>
			${len(a.albums)} альбомов
			</span>
			<p>
				${a.descr}
			</p>
		</div>
% endfor
		<div style="clear: both"></div>
	</div>
</div>
% endif

% if c.photos:
	<div class="gallery-thumbs">
% for p in c.photos:
		<div class="gallery-thumb">
			<a href='${h.url_for(controller="/photo", aid=p.album_id, pid=p.id)}'>
				<img alt="${p.display_name}" src="${c.u.get_web_preview_path(p)}"/>
			</a>
% if c.admin:
			<br/>
			${h.link_to("del", h.url_for(controller = "admin", action = "photo_del_submit", pid = p.id))}
% endif
		</div>
% endfor
		<div style="clear: both"></div>
	</div>
% elif not c.albums:
	<h2>There is not photos in this album</h2>
% endif
</div>
