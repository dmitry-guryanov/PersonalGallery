<%def name="photoNavBar(nav)">
<div id="photo-header">
	<div id="photo-counter">
		${nav.index + 1}/${nav.count}
	</div>
	<div id="photo-menu">
	% for tag in ["first", "prev", "next", "last"]:
		<div onmouseover="highlight('${tag}', true)" onmouseout="highlight('${tag}', false)">
	% if getattr(nav, tag):
	<% p = getattr(nav, tag) %>
			<a onClick="showPhoto('${p.get_web_path()}', ${p.width}, ${p.height})"
					href='${url.current(pid=getattr(nav, tag).id)}'>
				<img id="nav-${tag}" src="/gallery-static/i/${tag}.png"/>
			</a>
	%endif
		</div>
	%endfor
	</div>
</div>
</%def>
