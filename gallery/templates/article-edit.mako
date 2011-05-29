<%inherit file="base.mako"/>

<%def name="head()">
</%def>

<%def name="header()">
<%include file="header.mako"/>
</%def>


<div class="prefs-page">

% if new_article:
<h3>Create new article</h3>
% else:
<h3>Edit article</h3>
% endif

<div class="main_content">
<div class="prefs-box">

% if new_article:
${h.form(url(root.article, "commitnew"), method='post', multipart=True)}
% else:
${h.form(url(article, "commitedit"), method='post', multipart=True)}
% endif

% if new_article:
${h.hidden('new_article', value = 1)}
% endif

<div>
<h4>Title</h4>
${h.text('title', value = article.title, size = 40)}<br/>
</div>

<h4>Content</h4>
${h.textarea('body', article.body, cols=120, rows=40)}<br/>
</div>


<br/>
% if new_article:
${h.submit('commit', 'Create')}
% else:
${h.submit('commit', 'Save')}
% endif

${h.submit('cancel', 'Cancel')}
</div>

${h.end_form()}

</div>
</div>

</div>
