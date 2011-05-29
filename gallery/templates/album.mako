## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%namespace name="photonav" file="album-photonav.mako"/>

<%def name="head()">
% if photo:
<script type="text/javascript" src="/static/js/gallery.js"></script>
<script type="text/javascript">

side_margin = 10;
top_margin = 10;
bottom_margin = 1;
border = 50;

function complete(s) {
	navbar = document.getElementById("photo-navbar");
	header = document.getElementById("photo-header");
	header.parentNode.removeChild(header);

	navbar.innerHTML = s;

	photo = document.getElementById("mainphoto");
	photo.useMap = "#prevnext";

	size = getViewportSize();
	resizeMapAreas(photo);
	setControlsPosition(size);

	window.location.hash = document.getElementById("current-url").innerHTML;
}

function getViewportSize() {
	var size = {
		w: getWidth() - 2 * side_margin,
		h: getHeight() - top_margin - bottom_margin,
	}

	if(size.w < 600)
		size.w = 600;
	if(size.h < 400)
		size.h = 400;

	return size;
}

function resizePhoto(photo, size) {
	scale = getScale(size.w - 2 * border, size.h - 2 * border, origWidth, origHeight);

	photo_width = scale * origWidth;
	photo.style.width = photo_width + "px";
	photo_height = scale * origHeight;
	photo.style.height = photo_height + "px";

	/* center image */
	if(size.w > photo_width + 2 * border)
		photo.style.left = side_margin - border + (size.w - photo_width) / 2 + "px";
	else
		photo.style.left = side_margin + "px";
	
	if(size.h - 40 > photo_height + 2 * border)
		photo.style.top = top_margin + (size.h - 40 - photo_height) / 2 - border + "px";
	else
		photo.style.top = top_margin + "px";
}

function setControlsPosition(size) {
	/* center photo navigation bar */
	menu = document.getElementById("photo-menu");
	menu.style.left = (size.w / 2 + side_margin - 160) + "px";
}

function resizeMapAreas(photo) {
	width = photo.style.width.replace("px", "");
	height = photo.style.height.replace("px", "");

	coords = "0,0," + width / 3 + "," + height;
	document.getElementById("prev-rect").coords = coords;

	coords = width * 2 / 3 + ",0," + width + "," + height;
	document.getElementById("next-rect").coords = coords;
}

function onResize(event) {
	size = getViewportSize();
	photo = document.getElementById("mainphoto");

	resizePhoto(photo, size);
	resizeMapAreas(photo);
	setControlsPosition(size);
}

function unhidePhoto() {
	document.getElementById('mainphoto').style.display="block";
}

function showPhoto(url, path, width, height) {
	img1 = document.getElementById("mainphoto");
	img1.id = "mainphoto-old";

	img2 = new Image();
	img2.src = path;
	img2.id = "mainphoto";
	img2.style.display = "none";
	document.getElementById("mainphoto-container").appendChild(img2);
	img2.onLoad = unhidePhoto();

	origWidth = width;
	origHeight = height;
	onResize(0);

	img1.parentNode.removeChild(img1);

	loadXMLDoc(url, complete);
}

var origWidth;
var origHeight;

function onload() {
	origWidth = document.getElementById("origWidthEl").value;
	origHeight = document.getElementById("origHeightEl").value;
	ret = initialiseStateFromURL();
	if(ret)
		return 0;
	onResize();
	unhidePhoto();
}

//Event.observe(window, 'resize', function (e) { window.alert("qwe");});
window.onresize = onResize;

if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", onload, false);
} else {
	window.onload = onload;
}

function highlight(tag, f) {
	if(f)
		hover = "-hover"
	else
		hover = "";

	document.getElementById("nav-" + tag).src = "/static/i/" + tag + hover + ".png";
}

</script>
% endif
</%def>

<%def name="header()">
<%include file="header.mako"/>
% if admin:
	<div>
	<div class="admin_navibar">
	${h.link_to("edit album", url(album, "edit"))}
	${h.link_to("delete album", url(album, "commitdel"))}
	${h.link_to("add album", url(album, "new"))}
	${h.link_to("add photo", url(album, "addphoto"))}
	${h.link_to("logout", url(root.login, "logout"))}
	</div>
	</div>
% endif
</%def>


<div class="pager">${albums.pager()}</div>
% if albums:
	<div class="gallery-albums"><div class="gallery-albums2">
<% i = 0 %>
% for a in albums:
		<div class="gallery-album">
			<a class="gallery-thumb-link" href='${url(a)}'>
				<img  alt="${a.display_name}" src="${a.get_web_thumb()}"/>
			</a>
			<span class="album-link">
				<a href='${url(a)}'>
					${a.display_name}
				</a>
			</span><br/>
			<span class="meta">
% if counts[a.id][1] > 0:
				${counts[a.id][1]} ${h.get_mult_word("photo", counts[a.id][1])}
% endif
% if counts[a.id][0] > 0:
				${counts[a.id][0]} ${h.get_mult_word("album", counts[a.id][0])}
% endif

			</span>
			<p>${a.descr}</p>
		</div>
% endfor
		<div style="clear: both"></div>
	</div></div>
% endif

<div class="pager">${photos.pager()}</div>
% if photos:
	<div class="gallery-thumbs"><div class="gallery-thumbs2">
	<div id="album-photos-menu">посмотреть
##		<a href="${url(controller = 'photo', action = 'index', aid = album.id, pid = photos[0].id)}">по одной</a> или
		<a href="${url(album, 'allphotos')}">все сразу</a>
	</div>
% for p in photos:
		<span>
			<a href='${url(root.photo, str(p.id))}'>
				<img src="${p.get_web_preview_path()}"/>
			</a>
% if admin:
			${h.link_to("del", url(p, "commitdel"))}
			${h.link_to("edit", url(p, "edit"))}
% endif
		</span>
% endfor
		<div style="clear: both"></div>
	</div>
		<div style="clear: both"></div>
<div class="pager">${photos.pager()}</div>
	</div>
% elif not albums:
	<h2>There are no photos in this album</h2>
% endif


% if photo:
<div class="overlay"></div>

<div style="z-index: 11;">
<div id="photo-close">
	<a href="${url(album)}">
		<img alt="close" id="nav-close"
			onmouseover="highlight('close', true)" onmouseout="highlight('close', false)"
		src="/static/i/close.png">
	</a>
</div>

<div id="photo-navbar">
	${photonav.photoNavBar(nav = pnav)}
</div>

<div id="mainphoto-container">
<img id="mainphoto" style="display:none" src='${photo.get_web_path()}' usemap="#prevnext"/>
</div>
<input id="origWidthEl" type="hidden" value="${photo.width}" />
<input id="origHeightEl" type="hidden" value="${photo.height}" />

% endif
