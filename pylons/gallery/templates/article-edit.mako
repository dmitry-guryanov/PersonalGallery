<%inherit file="base.mako"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>


<div class="prefs-page">

<h3>Edit photo properties</h3>
<div class="main_content">
<div class="prefs-box">

${h.secure_form(url('articles'), method='post', multipart=True)}

<div>
<h4>Title</h4>
${h.text('title', value = '', size = 40)}<br/>
</div>



<br/>
${h.submit('enter', 'Change')}
${h.submit('cancel', 'Cancel')}
</div>

${h.end_form()}

</div>
</div>

</div>
