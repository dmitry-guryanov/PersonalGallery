
<div id="header">
<table id="menu" cellspacing="0"><tr>
	<td id="logo"><a href="${url(controller='album', action='index')}">Фотограф Дмитрий Гурьянов</a>
	<p>тел: 8 915 218-83-54, icq: 227-412-816<br/> e-mail: dmitry.guryanov@gmail.com</p>
</td>
	<td>
<%
links = []
for a in c.top_albums:
	links.append(h.link_to(a.display_name,
			url(controller="album", action = "show_first_page", aid=a.id)))
s = "&nbsp;|&nbsp;".join(links)
%>
	${s | n}
	</td>
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
