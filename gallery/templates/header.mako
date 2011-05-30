
<div id="header">
<div id="menu">
	<div id="logo"><a href="${url(root)}">Фотограф Дмитрий Гурьянов</a>
	<p>тел: 8 915 218-83-54, icq: 227-412-816<br/> e-mail: dmitry.guryanov@gmail.com</p>
</div>
	<div>
<%
links = []
for link in top_links:
	links.append("<a href=\"%s\">%s</a>" % (link.url, link.name))
s = "&nbsp;|&nbsp;".join(links)
%>
	${s | n}
	</div>
</div>
</div>

