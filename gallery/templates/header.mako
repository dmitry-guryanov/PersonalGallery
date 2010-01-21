<div class="main-header">${h.link_to("Dmitry Guryanov\'s gallery", url(controller='album'))}</div>

<!-- ######  navibar ###### -->
<div>
	<div class="navibar">
	% for a in c.top_albums:
		<div class="navibar-item">
			${h.link_to(a.display_name,
					url(controller="album", action = "show_first_page", aid=a.id))}
		</div>
	% endfor
	</div>
</div>
<!-- ######  /navibar ###### -->
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
