## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Dmitry Guryanov's gallery</title>
	${h.stylesheet_link('/gallery-static/css/style.css')}
<script type="text/javascript">

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
	alert(s);
}

function clicked() {
	loadXMLDoc('${url.current(action = "req")}', complete);
}

</script>
</head>

<body>

Hello, welcome to the wonderful ping! controller! 

<div onclick="clicked();" style="width:100px; height: 100px; background: green;"></div>
<div id="pongbox"></div>


</body>
</html>

