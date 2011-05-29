<%def name="hlProps(tag)"> \
onmouseover="highlight('${tag}', true)" onmouseout="highlight('${tag}', false)" \
</%def>


<%def name="aProps(p)"> \
<%
if not p:
	return
purl = url(p, "getajax");
%> \
onClick="showPhoto('${purl}', '${p.get_web_path()}', ${p.width}, ${p.height})" \
</%def>


<%def name="navButton(tag, p)">
<div ${hlProps(tag)}>
<%
if p:
	img_tags = ""
else:
	img_tags = 'style="display:none;"'
%>	<a id="link-${tag}" ${aProps(p)}>
		<img id="nav-${tag}" ${img_tags | n} src="/static/i/${tag}.png"/>
	</a>
</div>
</%def>


<%def name="photoNavBar(nav)">
<div id="photo-header">
	<div id="photo-counter">
		${nav.index + 1}/${nav.count}
	</div>
	<div id="photo-menu">
	% for tag in ["first", "prev", "next", "last"]:
		${navButton(tag, getattr(nav, tag))}
	%endfor
	</div>

<%
#FIXME
from urlparse import urlparse
current_url = urlparse(url(nav.photo)).path
%>
	<div id="current-url" style="display: none;">${current_url}</div>

% if nav.prev:
	<img id="prev-photo" style="display: none" src="${nav.prev.get_web_path()}"/>
% endif
% if nav.next:
	<img id="next-photo" style="display: none" src="${nav.next.get_web_path()}"/>
% endif

<map id="prevnext" name="prevnext">
	<area ${hlProps("prev")} coords="0,0,0,0" ${aProps(nav.prev)} id="prev-rect" shape="rect"/>
	<area ${hlProps("next")} coords="0,0,0,0" ${aProps(nav.next)} id="next-rect" shape="rect"/>
</map>

</div>
</%def>

