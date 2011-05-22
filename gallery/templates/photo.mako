## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Dmitry Guryanov's gallery</title>
	${h.stylesheet_link('/gallery-static/css/style.css')}
<script type="text/javascript">

side_margin = 40;
top_margin = 10;
bottom_margin = 56;

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
	scale = get_scale(width, height, size.width, size.height);
	/* document.getElementById("demo").innerHTML=window.innerWidth + "x" + window.innerHeight + " " + scale; */

	photo_width = scale * size.width;
	photo.style.width = photo_width + "px";
	photo_height = scale * size.height;
	photo.style.height = photo_height + "px";

	/* document.getElementById("demo2").innerHTML=width + "x" + height + " " + photo_width + "x" + photo_height */

	/* center image */
	if(width > photo_width)
		photo.style.left = side_margin + (width - photo_width) / 2 + "px";
	else
		photo.style.left = side_margin + "px";
	
	if(height > photo_height)
		photo.style.top = top_margin + (height - photo_height) / 2 + "px";
	else
		photo.style.top = top_margin + "px";

	/* update image map */
% if c.prev:
	coords = "0,0," + photo_width / 3 + "," + photo_height;
	document.getElementById("prev-rect").coords = coords;
% endif
% if c.next:
	coords = photo_width * 2 / 3 + ",0," + photo_width + "," + photo_height;
	document.getElementById("next-rect").coords = coords;
% endif

	document.getElementById("photo-header").style.top = (window.innerHeight - 46) + "px";
}

window.onresize = onresize;
</script>
</head>

<body onload="onresize();">

<!--
<div id="demo"> </div>
<div id="demo2"> </div> -->

<div id="photo-close">
	<a href="${url(controller='album', action='show_first_page', aid=c.photo.album_id)}"><img src="/gallery-static/i/close.png"></a>
</div>

<div id="photo-header">
	<div id="photo-counter">
		${c.idx}/${c.all}
	</div>
	<div id="photo-menu">
	% for tag in ["first", "prev", "next", "last"]:
		<div>
		% if getattr(c, tag):
			<a href='${url.current(pid=getattr(c, tag).id)}'><img src="/gallery-static/i/${tag}.png"/></a>
		%endif
		</div>
	%endfor
	</div>

</div>

<div class="photo"><div class="photo2">

<img id="mainphoto" alt="" src='${c.photo.get_web_path()}' usemap="#prevnext" width="${c.photo.width}" height="${c.photo.height}"/>
<img id="mainphotosize" style="display:none;" width="${c.photo.width}" height="${c.photo.height}" onload="onresize();"/>

</div></div>

<map id="prevnext" name="prevnext">
% if c.prev:
<area id="prev-rect" shape="rect" coords="0,0,${c.photo.width / 3},${c.photo.height}"
href='${url.current(pid=c.prev.id)}'
alt="IMG_0161"/>
% endif

% if c.next:
<area id="next-rect" shape="rect" coords="${c.photo.width * 2 / 3},0,${c.photo.width},${c.photo.height}"
href='${url.current(pid=c.next.id)}'
alt="IMG_0161"/>
% endif
</map>

</body>
</html>
