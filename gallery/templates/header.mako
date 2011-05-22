
<div id="header">
<table id="menu" cellspacing="0"><tr>
	<td id="logo"><a href="${url(controller='album', action='index')}">фотограф Дмитрий Гурьянов</a></td>
	% for a in c.top_albums:
	<td>${h.link_to(a.display_name, url(controller="album", action = "show_first_page", aid=a.id))}</td>
	% endfor
	<td id="search"></td>
</tr></table>
</div>

% if c.admin:
	${h.auth_token_hidden_field()}
	<div>
	<div class="admin_navibar">
	${h.link_to("edit album", url.current(controller="admin", action="album_edit"))}
	${h.link_to("delete album", url.current(controller="admin", action="album_del"))}
	${h.link_to("add album", url.current(controller="admin", action="album_add"))}
	${h.link_to("add photo", url.current(controller="admin", action="photo_add"))}
	${h.link_to("logout", url.current(controller="login", action="logout"))}
	</div>
	</div>
% endif
