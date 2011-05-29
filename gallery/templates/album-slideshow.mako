## -*- coding: utf-8 -*-
<%inherit file="base.mako"/>
<%def name="head()">
<link rel="stylesheet" href="/static/css/coin-slider-styles.css" type="text/css" media="screen" charset="utf-8"/>
<script type="text/javascript" src="/static/js/jquery-1.6.1.js"></script>
<script type="text/javascript" src="/static/js/coin-slider.js"></script>

<script type="text/javascript">

$(document).ready(function() {
	$('#slideshow').coinslider({ width: 900, height: 600});
});

</script>

</%def>
<%def name="header()">
<%include file="header.mako"/>
</%def>

<div style="text-align: center;">
<div style="display: inline-block;">
	<div style="display:block" id="slideshow">
% for p in photos:
		<a href="${'img-%d' % p.id}" target="_blank">
			<img alt="${p.display_name}" src="${p.get_web_path()}"/>
		</a>
% endfor
	</div>
</div>
</div>

