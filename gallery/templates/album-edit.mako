<%inherit file="base.mako"/>

<%def name="head()">
</%def>
<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

% if new_album:
<h3>New album properties</h3>
% else:
<h3>Edit album properties</h3>
% endif
<div class="main_content">
<div class="prefs-box">

${h.form(url(album, "commitedit"), method='post', multipart=True)}

% if new_album:
${h.hidden('new_album', value = 1)}
% endif

<div>
<h4>Name</h4>
${h.text('name', value = album.name, size = 40)}<br/>
</div>

<div>
<h4>Title</h4>
${h.text('title', value = album.display_name, size = 40)}<br/>
</div>

<div>
<h4>Description</h4>
${h.text('description', value = album.descr, size = 80)} <br/>
</div>

<div>
<h4>Hide album</h4>
<p>Hidden items are not visible to guest users until the page for the item is accessed directly.</p>
${h.checkbox('hide_album', id='hide_album', checked = album.hidden)} <label for="hide_album">Hidden</label>
</div>

<div>
<h4>Sort by</h4>
${h.select('sort_by', album.sort_by, h.sorting_names.items(), id='sort_by')}
</div>

<div>
<h4>Thumbnail for the album</h4>
<p>The file uploaded will be resized to thumbnail size and shown on album page</p>
${h.file('album_thumbnail', size = 40)}<br/>
</div>
<br/>
<div>
% if new_album:
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
