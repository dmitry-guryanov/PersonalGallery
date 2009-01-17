
<%inherit file="base.html"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>

<div class="photo">
% if c.prev:
	<a href='${h.url_for(controller="photo", aid=c.prev.album_id, pid=c.prev.id)}'
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
	<a href='${h.url_for(controller="photo", aid=c.next.album_id, pid=c.next.id)}'
		id="nextArrow"
		style="position: absolute;
	            margin: 15px 0 0 60%;
				visibility: hidden"
				onmouseover="document.getElementById('nextArrow').style.visibility='visible'"
				onmouseout="document.getElementById('nextArrow').style.visibility='hidden'">
			<img src="/gallery-static/i/arrow-right.gif" alt="" width="20" height="17"/>
	</a>
% endif

<img alt="" src='${c.u.get_web_photo_path(c.photo)}' usemap="#prevnext" width="${c.photo.width}" height="${c.photo.height}" class="gallery-photo"/>

</div>

<map id="prevnext" name="prevnext">


% if c.prev:
<area shape="rect" coords="0,0,${c.photo.width / 3},${c.photo.height}"
href='${h.url_for(controller="photo", aid=c.prev.album_id, pid=c.prev.id)}'
alt="IMG_0161"
onmouseover="document.getElementById('prevArrow').style.visibility='visible'"
onmouseout="document.getElementById('prevArrow').style.visibility='hidden'"/>
% endif

% if c.next:
<area shape="rect" coords="${c.photo.width * 2 / 3},0,${c.photo.width},${c.photo.height}"
href='${h.url_for(controller="photo", aid=c.next.album_id, pid=c.next.id)}'
alt="IMG_0161"
onmouseover="document.getElementById('nextArrow').style.visibility='visible'"
onmouseout="document.getElementById('nextArrow').style.visibility='hidden'"/>
% endif

</map>

