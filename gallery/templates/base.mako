## -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Dmitry Guryanov's gallery</title>
	${h.stylesheet_link('/gallery-static/css/style.css')}
</head>

<body>
	<!-- HEADER -->
		${self.header()}
	<!-- HEADER -->


	<div id="page">	<!-- MAIN-CONTENT -->

	${self.body()}

	</div>	<!-- MAIN-CONTENT -->


	<div class="footer">	<!-- FOOTER -->
		${self.footer()}
	</div>	<!-- FOOTER -->
</body>

<%def name="footer()">
    <div style="font-size: 8pt; padding: 20px 70px 20px 20px; text-align: right">©Дмитрий Гурьянов, +7 915 218-83-54, ICQ: 227412816</div>
</%def>
</html>

