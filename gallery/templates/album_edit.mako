
<%inherit file="base.html"/>

<%def name="header()">
</%def>

album view<br/>

album: ${c.album}<br/>
page: ${c.page}<br/>

% if c.admin:
	<a href = '/album_edit/${c.album}'>edit</a>
% endif

% for a in c.albums:
	<ul><a href='/album/${a.id}'>${unicode(a.display_name, 'utf-8')}</a></ul>
% endfor

% for p in c.photos:
	<ul><a href="/photo/${p.album_id}/${p.name}"><img src="/photos/${p.album_id}/previews/${p.path}"/></a></ul>
% endfor

<a href="/admin/photo_add/${c.album}">add photo</a>
