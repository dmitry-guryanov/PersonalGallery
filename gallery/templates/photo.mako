## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>

<%def name="header()">
</%def>

${h.link_to(_(u"up to album"), url(controller="album", action="show_first_page", aid=c.photo.album_id))}

<div class="photo">
% if c.prev:
	<a href='${url.current(pid=c.prev.id)}'
		id="prevArrow"
		style="position: absolute;
	            margin: 15px 0 0 35%;
				visibility: hidden"
				onmouseover="document.getElementById('prevArrow').style.visibility='visible'"
				onmouseout="document.getElementById('prevArrow').style.visibility='hidden'">
			<img src="/gallery-static/i/arrow-left.gif" alt="" width="20" height="17"/>
	</a>
% endif

% if c.next:
	<a href='${url.current(pid=c.next.id)}'
		id="nextArrow"
		style="position: absolute;
	            margin: 15px 0 0 60%;
				visibility: hidden"
				onmouseover="document.getElementById('nextArrow').style.visibility='visible'"
				onmouseout="document.getElementById('nextArrow').style.visibility='hidden'">
			<img src="/gallery-static/i/arrow-right.gif" alt="" width="20" height="17"/>
	</a>
% endif

<img alt="" src='${c.photo.get_web_path()}' usemap="#prevnext" width="${c.photo.width}" height="${c.photo.height}" class="gallery-photo"/>

</div>

<map id="prevnext" name="prevnext">


% if c.prev:
<area shape="rect" coords="0,0,${c.photo.width / 3},${c.photo.height}"
href='${url.current(pid=c.prev.id)}'
alt="IMG_0161"
onmouseover="document.getElementById('prevArrow').style.visibility='visible'"
onmouseout="document.getElementById('prevArrow').style.visibility='hidden'"/>
% endif

% if c.next:
<area shape="rect" coords="${c.photo.width * 2 / 3},0,${c.photo.width},${c.photo.height}"
href='${url.current(pid=c.next.id)}'
alt="IMG_0161"
onmouseover="document.getElementById('nextArrow').style.visibility='visible'"
onmouseout="document.getElementById('nextArrow').style.visibility='hidden'"/>
% endif

</map>

