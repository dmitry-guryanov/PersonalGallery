## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%def name="header()">
<%include file="header.mako"/>
</%def>


<div class="pager">${c.albums.pager()}</div>
% if c.albums:
	<div class="gallery-albums"><div class="gallery-albums2">
<% i = 0 %>
% for a in c.albums:
		<div class="gallery-album">
			<a class="gallery-thumb-link" href='${url(controller="album", action="show_first_page", aid=a.id)}'><img  alt="${a.display_name}" src="${a.get_web_thumb()}"/></a>
			<span class="album-link"><a href='${url(controller="album", action="show_first_page", aid=a.id)}'>${a.display_name}</a></span><br/>
			<span class="meta">
% if c.counts[a.id][1] > 0:
				${c.counts[a.id][1]} ${c.u.get_mult_word("photo", c.counts[a.id][1])}
% endif
% if c.counts[a.id][0] > 0:
				${c.counts[a.id][0]} ${c.u.get_mult_word("album", c.counts[a.id][0])}
% endif

			</span>
			<p>${a.descr}</p>
		</div>
% endfor
		<div style="clear: both"></div>
	</div></div>
% endif

<div class="pager">${c.photos.pager()}</div>
% if c.photos:
	<div class="gallery-thumbs"><div class="gallery-thumbs2">
	<div id="album-photos-menu">посмотреть <a href="${url(controller = 'photo', action = 'index', aid = c.album.id, pid = c.photos[0].id)}">по одной</a> или
		<a href="${url(controller = 'album', action = 'show_photos', aid = c.album.id)}">все сразу</a>
	</div>
% for p in c.photos:
			<a href='${url(controller="photo", action="index", aid=p.album_id, pid=p.id)}'>
				<img src="${p.get_web_preview_path()}"/>
			</a>
% if c.admin:
			${h.link_to("del", url(controller = "admin", action = "photo_del_submit", aid = c.album.id, pid = p.id))}
			${h.link_to("edit", url(controller = "admin", action = "photo_edit", aid = c.album.id, pid = p.id))}
			<br/>
% endif
% endfor
		<div style="clear: both"></div>
	</div>
		<div style="clear: both"></div>
<div class="pager">${c.photos.pager()}</div>
	</div>
% elif not c.albums:
	<h2>There are no photos in this album</h2>
% endif

