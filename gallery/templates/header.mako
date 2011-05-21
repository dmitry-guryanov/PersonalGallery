
<!--
<div id="header">
<div id="menu">
	<ul>
	<li id="logo"><a href="${url(controller='album', action='index')}">фотограф Дмитрий Гурьянов</a></li>

	% for a in c.top_albums:
		<li>${h.link_to(a.display_name, url(controller="album", action = "show_first_page", aid=a.id))}</li>
	% endfor
	</ul>
</div>
</div>
-->


<div id="header2">
<table id="menu2" cellspacing="0"><tr>
	<td id="logo2"><a href="${url(controller='album', action='index')}">фотограф Дмитрий Гурьянов</a></td>

<!-- ######  navibar ###### -->
	% for a in c.top_albums:
		<td>${h.link_to(a.display_name, url(controller="album", action = "show_first_page", aid=a.id))}</td>
	% endfor
<!-- ######  /navibar ###### -->
	<td id="search2"></td>
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
