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

function initialiseStateFromURL() {
	if(window.location.hash) {
		tmp = window.location.hash.slice(1);
		window.location.hash = "";
		window.location.pathname = tmp;
		return 1;
	} else
		return 0;
}

