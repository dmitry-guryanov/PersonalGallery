<div class="main-header">Dmitry Guryanov's gallery</div>
<!-- ######  navibar ###### -->
<div align=center>
<div class="navibar" align=center>
% for a in c.top_albums:
	<div class="navibar-item">
		${h.link_to(unicode(a.display_name, 'utf-8'), h.url_for(controller="/album", action = "show_first_page", aid=a.id))}
	</div>
% endfor

<br/>
</div>
</div>
<!-- ######  /navibar ###### -->
