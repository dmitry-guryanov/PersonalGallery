<%inherit file="base.html"/>
<%def name="header()">
</%def>

<%include file="header.mako"/>

% if c.albums:
<div class="gallery-thumbs">
% for a in c.albums:
	<div class="gallery-thumb-album">
		${h.link_to(unicode(a.display_name, 'utf-8'), h.url_for(controller="/album", action="show_first_page", aid=a.id))}
	</div>
% endfor
</div>
% endif

% if c.photos:
<table class="gallery-thumbs" align="center">
% for i in range(len(c.photos)):
<%
	p = c.photos[i]
%>
%	if i % 4 == 0:
	<tr>
%	endif
		<td class="gallery-thumb">
			<a class="gallery-thumb-link" href='${h.url_for(controller="/photo", aid=p.album_id, pid=p.id)}'><img alt="${p.display_name}" src="${c.u.get_web_preview_path(p)}"/></a>
% if c.admin:
			<br/>
			${h.link_to("del", h.url_for(controller = "admin", action = "photo_del_submit", pid = p.id))}
% endif
		</td>
%	if i % 4 == 3 or i == len(c.photos) - 1:
	</tr>
%	endif
% endfor
</table>

% elif not c.albums:
	<h2>There is not photos in this album</h2>
% endif

