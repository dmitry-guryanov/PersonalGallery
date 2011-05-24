## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>


<%def name="head()">
% if hasattr(c, "photo"):
<script type="text/javascript">

side_margin = 10;
top_margin = 10;
bottom_margin = 1;
border = 50;

function get_scale(pw, ph, w, h) {
	xscale = pw / w;
	yscale = ph / h;

	scale = Math.min(xscale, yscale);
	if (scale < 1)
		return scale;
	else
		return 1;

}

function onresize(event) {
	photo = document.getElementById("mainphoto")
	size = document.getElementById("mainphotosize")

	width = window.innerWidth - 2 * side_margin;
	height = window.innerHeight - top_margin - bottom_margin;

	if(width < 600)
		width = 600;
	if(height < 400)
		height = 400;

//	document.getElementById("photo-header").style.top = (height + top_margin + 10) + "px";
	document.getElementById("photo-menu").style.left = (width / 2 + side_margin - 160) + "px";

	scale = get_scale(width - 2 * border, height - 2 * border, size.width, size.height);

	photo_width = scale * size.width;
	photo.style.width = photo_width + "px";
	photo_height = scale * size.height;
	photo.style.height = photo_height + "px";

	/* center image */
	if(width > photo_width + 2 * border)
		photo.style.left = side_margin -border + (width - photo_width) / 2 + "px";
	else
		photo.style.left = side_margin + "px";
	
	if(height - 40 > photo_height + 2 * border)
		photo.style.top = top_margin + (height -40 - photo_height) / 2 - border + "px";
	else
		photo.style.top = top_margin + "px";

	photo.style.display="block";

	/* update image map */
% if c.prev:
	coords = "0,0," + photo_width / 3 + "," + photo_height;
	document.getElementById("prev-rect").coords = coords;
% endif
% if c.next:
	coords = photo_width * 2 / 3 + ",0," + photo_width + "," + photo_height;
	document.getElementById("next-rect").coords = coords;
% endif
}

if (document.images) {
% if c.prev:
img1 = new Image();
img1.src = "${c.prev.get_web_path()}";
% endif
% if c.next:
img2 = new Image();
img2.src = "${c.next.get_web_path()}";
% endif
}

//Event.observe(window, 'resize', function (e) { window.alert("qwe");});
window.onresize = onresize;

if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", onresize, false);
} else {
	window.onload = onresize;
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
			<a class="gallery-thumb-link" href='${url(controller="album", action="show_first_page", aid=a.id)}'><img  alt="${a.display_name}" src="${a.get_web_thumb()}"/></a>
			<span class="album-link"><a href='${url(controller="album", action="show_first_page", aid=a.id)}'>${a.display_name}</a></span><br/>
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
	<div id="album-photos-menu">посмотреть <a href="${url(controller = 'photo', action = 'index', aid = c.album.id, pid = c.photos[0].id)}">по одной</a> или
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
		<img alt="close" id="nav-close" onmouseover="highlight('close', true)" onmouseout="highlight('close', false)" src="/gallery-static/i/close.png"></a>
</div>

<div id="photo-header">
	<div id="photo-counter">
		${c.idx}/${c.all}
	</div>
	<div id="photo-menu">
	% for tag in ["first", "prev", "next", "last"]:
	<div onmouseover="highlight('${tag}', true)" onmouseout="highlight('${tag}', false)">
	% if getattr(c, tag):
		<a href='${url.current(pid=getattr(c, tag).id)}'><img id="nav-${tag}" src="/gallery-static/i/${tag}.png"/></a>
	%endif
	</div>
	%endfor
	</div>
</div>

<img id="mainphoto" alt="" style="display:none" src='${c.photo.get_web_path()}' usemap="#prevnext" width="${c.photo.width}" height="${c.photo.height}"/>
<img id="mainphotosize" style="display:none;" width="${c.photo.width}" height="${c.photo.height}"/>
</div>

<map id="prevnext" name="prevnext">
% if c.prev:
<area onmouseover="highlight('prev', true)" onmouseout="highlight('prev', false)" id="prev-rect" shape="rect" href='${url.current(pid=c.prev.id)}'/>
% endif
% if c.next:
<area onmouseover="highlight('next', true)" onmouseout="highlight('next', false)" id="next-rect" shape="rect" href='${url.current(pid=c.next.id)}'/>
% endif

% endif
