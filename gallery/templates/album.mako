## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%namespace name="photonav" file="album-photonav.mako"/>


<%def name="head()">
% if hasattr(c, "photo"):
<script type="text/javascript">

side_margin = 10;
top_margin = 10;
bottom_margin = 1;
border = 50;

function loadXMLDoc(url, func) {
	var xmlhttp;
	if (window.XMLHttpRequest) {
		// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	} else {
		// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	xmlhttp.onreadystatechange=function() {
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
			func(xmlhttp.responseText);
		}
	}

	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function complete(s) {
	parent = document.getElementById("photo-navbar");
	header = document.getElementById("photo-header");
	parent.removeChild(header);


	parent.innerHTML = s;

	width = getWidth() - 2 * side_margin;

	if(width < 600)
		width = 600;

	/* center photo navigation bar */
	menu = document.getElementById("photo-menu");
	menu.style.left = (width / 2 + side_margin - 160) + "px";

	photo = document.getElementById("mainphoto");
	photo.useMap = "#prevnext";
	onresize();
	window.location.hash = document.getElementById("current-url").innerHTML;
}

function getScale(pw, ph, w, h) {
	xscale = pw / w;
	yscale = ph / h;

	scale = Math.min(xscale, yscale);
	if (scale < 1)
		return scale;
	else
		return 1;
}

function getWidth()
{
	if (window.innerWidth)
		return window.innerWidth;
	else if (document.documentElement && document.documentElement.clientWidth)
		return document.documentElement.clientWidth;
	else if (document.body)
		screenWidth=document.body.clientWidth;
	else
		return 1000;
}

function getHeight()
{
	if (window.innerHeight)
		return window.innerHeight;
	else if (document.documentElement && document.documentElement.clientHeight)
		return document.documentElement.clientHeight;
	else if (document.body)
		screenHeight=document.body.clientHeight;
	else
		return 1000;
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

function initialiseStateFromURL() {
	if(window.location.hash) {
		tmp = window.location.hash.slice(1);
		window.location.hash = "";
		window.location.pathname = tmp;
		return 1;
	} else
		return 0;
}

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

	document.getElementById("nav-" + tag).src = "/gallery-static/i/" + tag + hover + ".png";
}

</script>
% endif
</%def>

<%def name="header()">
<%include file="header.mako"/>
</%def>


<div class="pager">${c.albums.pager()}</div>
% if c.albums:
	<div class="gallery-albums"><div class="gallery-albums2">
<% i = 0 %>
% for a in c.albums:
		<div class="gallery-album">
			<a class="gallery-thumb-link" href='${url(controller="album", action="show_first_page", aid=a.id)}'>
				<img  alt="${a.display_name}" src="${a.get_web_thumb()}"/>
			</a>
			<span class="album-link">
				<a href='${url(controller="album", action="show_first_page", aid=a.id)}'>
					${a.display_name}
				</a>
			</span><br/>
			<span class="meta">
% if c.counts[a.id][1] > 0:
				${c.counts[a.id][1]} ${c.u.get_mult_word("photo", c.counts[a.id][1])}
% endif
% if c.counts[a.id][0] > 0:
				${c.counts[a.id][0]} ${c.u.get_mult_word("album", c.counts[a.id][0])}
% endif

			</span>
			<p>${a.descr}</p>
		</div>
% endfor
		<div style="clear: both"></div>
	</div></div>
% endif

<div class="pager">${c.photos.pager()}</div>
% if c.photos:
	<div class="gallery-thumbs"><div class="gallery-thumbs2">
	<div id="album-photos-menu">посмотреть
		<a href="${url(controller = 'photo', action = 'index', aid = c.album.id, pid = c.photos[0].id)}">по одной</a> или
		<a href="${url(controller = 'album', action = 'show_photos', aid = c.album.id)}">все сразу</a>
	</div>
% for p in c.photos:
			<a href='${url.current(action="show_photo", pid=p.id)}'>
				<img src="${p.get_web_preview_path()}"/>
			</a>
% if c.admin:
			${h.link_to("del", url(controller = "admin", action = "photo_del_submit", aid = c.album.id, pid = p.id))}
			${h.link_to("edit", url(controller = "admin", action = "photo_edit", aid = c.album.id, pid = p.id))}
			<br/>
% endif
% endfor
		<div style="clear: both"></div>
	</div>
		<div style="clear: both"></div>
<div class="pager">${c.photos.pager()}</div>
	</div>
% elif not c.albums:
	<h2>There are no photos in this album</h2>
% endif


% if hasattr(c, "photo"):
<div class="overlay"></div>

<div style="z-index: 11;">
<div id="photo-close">
	<a href="${url(controller='album', action='show_page', aid=c.photo.album_id, page = c.photos.page)}">
		<img alt="close" id="nav-close"
			onmouseover="highlight('close', true)" onmouseout="highlight('close', false)"
		src="/gallery-static/i/close.png">
	</a>
</div>

<div id="photo-navbar">
${photonav.photoNavBar(nav = c.pnav)}
</div>

<div id="mainphoto-container">
<img id="mainphoto" style="display:none" src='${c.photo.get_web_path()}' usemap="#prevnext"/>
</div>
<input id="origWidthEl" type="hidden" value="${c.photo.width}" />
<input id="origHeightEl" type="hidden" value="${c.photo.height}" />

% endif
