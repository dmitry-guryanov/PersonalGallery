<%inherit file="base.mako"/>

<%def name="head()">
</%def>
<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

<h3>Edit photo properties</h3>
<div class="main_content">
<div class="prefs-box">

${h.secure_form(url.current(action='photo_edit_submit'), method='post', multipart=True)}

<div>
<h4>Title</h4>
${h.text('title', value = c.photo.display_name, size = 40)}<br/>
</div>

<div>
<h4>Hide photo</h4>
<p>Hidden items are not visible to guest users until the page for the item is accessed directly.</p>
${h.checkbox('hide_photo', id='hide_photo', checked = c.photo.hidden)} <label for="hide_photo">Hidden</label>
</div>
<br/>
${h.submit('enter', 'Change')}
${h.submit('cancel', 'Cancel')}
</div>

${h.end_form()}

</div>
</div>

</div>
