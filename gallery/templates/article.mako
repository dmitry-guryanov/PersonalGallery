<%inherit file="base.mako"/>

<%def name="head()">
</%def>

<%def name="header()">
<%include file="header.mako"/>
% if admin:
	<div>
	<div class="admin_navibar">
	${h.link_to("edit article", url(article, "edit"))}
	${h.link_to("delete article", url(article, "commitdel"))}
	${h.link_to("add article", url(root.article, "new"))}
	${h.link_to("logout", url(root.login, "logout"))}
	</div>
	</div>
% endif
</%def>


<h1>${article.title}</h1>
<div style="text-align: right; font-size: 0.7em; font-style: italic;">
${article.created}
</div>

<div>
${article.get_body() | n}
</div>

</div>
