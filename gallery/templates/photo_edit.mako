<%inherit file="base.html"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

<h3>Edit photo properties</h3>
<div class="main_content">
<div class="prefs-box">

${h.form(url.current(action='photo_edit_submit'), method='post', multipart=True)}

<h4>Name</h4>
${h.text_field('name', value = c.photo.name, size = 40)}<br/>

<h4>Title</h4>
${h.text_field('title', value = c.photo.display_name, size = 40)}<br/>

<h4>Hide photo</h4>
<p>Hidden items are not visible to guest users until the page for the item is accessed directly.</p>
${h.check_box('hide_photo', id='hide_photo', checked = c.photo.hidden)} <label for="hide_photo">Hidden</label>

<h4>Image for displaying</h4>
<p>this image will be displayed in photo view page</p>
${h.file_field('photo_file', size = 40)}<br/>

<h4>Fullsize image</h4>
<p>This image will be available for downloading</p>
${h.file_field('photo_file_fullsize', size = 40)}<br/>
				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
${h.end_form()}

</div>
</div>

</div>
