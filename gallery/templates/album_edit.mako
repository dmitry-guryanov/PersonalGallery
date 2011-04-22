<%inherit file="base.mako"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

% if c.new_album:
<h3>New album properties</h3>
% else:
<h3>Edit album properties</h3>
% endif
<div class="main_content">
<div class="prefs-box">

${h.secure_form(url.current(action='album_edit_submit'), method='post', multipart=True)}

% if c.new_album:
${h.hidden('new_album', value = 1)}
% endif

<div>
<h4>Name</h4>
${h.text('name', value = c.album.name, size = 40)}<br/>
</div>

<div>
<h4>Title</h4>
${h.text('title', value = c.album.display_name, size = 40)}<br/>
</div>

<div>
<h4>Description</h4>
${h.text('description', value = c.album.descr, size = 80)} <br/>
</div>

<div>
<h4>Hide album</h4>
<p>Hidden items are not visible to guest users until the page for the item is accessed directly.</p>
${h.checkbox('hide_album', id='hide_album', checked = c.album.hidden)} <label for="hide_album">Hidden</label>
</div>

<div>
<h4>Sort by</h4>
<p>s</p>
${h.select('xx', "1", c.u.sorting_names.items(), id='sort_by')} <label for="sort_by">Hidden</label>
</div>


<div>
<h4>Thumbnail for the album</h4>
<p>The file uploaded will be resized to thumbnail size and shown on album page</p>
${h.file('album_thumbnail', size = 40)}<br/>


				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
</div>

${h.end_form()}

</div>
</div>

</div>
