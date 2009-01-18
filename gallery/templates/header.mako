<div class="main-header">${h.link_to("Dmitry Guryanov\'s gallery", h.url_for('/'))}</div>

<!-- ######  navibar ###### -->
<div align="center">
	<div class="navibar" align="center">
	% for a in c.top_albums:
		<div class="navibar-item">
			${h.link_to(a.display_name,
					h.url_for(controller="/album", action = "show_first_page", aid=a.id))}
		</div>
	% endfor
	<br/>
	</div>
</div>
<!-- ######  /navibar ###### -->
% if c.admin:
	<div align="center">
	<div class="admin_navibar" align="right">
	${h.link_to("edit album", h.url_for(controller="admin", action="album_edit"))}
	${h.link_to("delete album", h.url_for(controller="admin", action="album_del"))}
	${h.link_to("add album", h.url_for(controller="admin", action="album_add"))}
	${h.link_to("add photo", h.url_for(controller="admin", action="photo_add"))}
	${h.link_to("logout", h.url_for(controller="login", action="logout"))}
	</div>
	</div>
% endif

