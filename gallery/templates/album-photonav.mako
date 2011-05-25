<%def name="photoNavBar(nav)">
<div id="photo-header">
	<div id="photo-counter">
		${nav.index + 1}/${nav.count}
	</div>
	<div id="photo-menu">
	% for tag in ["first", "prev", "next", "last"]:
		<div onmouseover="highlight('${tag}', true)" onmouseout="highlight('${tag}', false)">
	% if getattr(nav, tag):
	<%
	p = getattr(nav, tag)
	purl = url(controller="album", action = "get_photo_ajax", aid = c.album.id, pid=p.id);
	%>
			<a id="link-${tag}" onClick="showPhoto('${purl}', '${p.get_web_path()}', ${p.width}, ${p.height})">
				<img id="nav-${tag}" src="/gallery-static/i/${tag}.png"/>
			</a>
	%else:
			<a id="link-${tag}">
			<img id="nav-${tag}" style="display:none;" id="nav-${tag}" src="/gallery-static/i/${tag}.png"/>
			</a>
	%endif
		</div>
	%endfor
	</div>

	<div id="current-url" style="display: none;">${url(controller="album", action = "show_photo", aid = c.album.id, pid=nav.photo.id, page = 0)}</div>

% if nav.prev:
	<img id="prev-photo" style="display: none" src="${nav.prev.get_web_path()}"/>
% endif
% if nav.next:
	<img id="next-photo" style="display: none" src="${nav.next.get_web_path()}"/>
% endif

<map id="prevnext" name="prevnext">
<area onmouseover="highlight('prev', true)"
	onmouseout="highlight('prev', false)"
	coords="0,0,0,0"
% if nav.prev:
<%
p = nav.prev
purl = url(controller="album", action = "get_photo_ajax", aid = c.album.id, pid=p.id);
%>
	onclick="showPhoto('${purl}', '${p.get_web_path()}', ${p.width}, ${p.height})"
% endif
	id="prev-rect" shape="rect"/>

<area onmouseover="highlight('next', true)"
	onmouseout="highlight('next', false)"
	coords="0,0,0,0"
% if nav.next:
<%
p = nav.next
purl = url(controller="album", action = "get_photo_ajax", aid = c.album.id, pid=p.id);
%>
	onclick="showPhoto('${purl}', '${p.get_web_path()}', ${p.width}, ${p.height})"
% endif
	id="next-rect" shape="rect"/>
</map>

</div>
</%def>

<!--					href='${url.current(pid=getattr(nav, tag).id)}'> -->
