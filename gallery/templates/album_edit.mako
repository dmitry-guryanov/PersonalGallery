
<%inherit file="base.html"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

<h3>Edit album properties</h3>
<div class="main_content">
<div class="prefs-box">

${h.form(h.url(action='album_edit_submit'), method='post')}
<h4>Name</h4>
${h.text_field('name', value = c.album.name, size = 40)}<br/>

<h4>Title</h4>
${h.text_field('title', value = unicode(str(c.album.display_name), 'utf-8'), size = 40)}<br/>


<h4>Description</h4>
${h.text_field('description', value = c.album.descr, size = 80)} <br/>

<h4>Hide album</h4>
<p>Hidden items are not visible to guest users until the page for the item is accessed directly.</p>
${h.check_box('hide_album', id='hide_album')} <label for="hide_album">Hidden</label>

<h4>Thumbnail for the album</h4>
<p>The file uploaded will be resized to thumbnail size and shown on album page</p>
${h.file_field('album_thubmnail', size = 40)}<br/>

				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
${h.end_form()}

</div>
</div>

</div>
