<%inherit file="base.html"/>
<%def name="header()">
</%def>
<%include file="header.mako"/>


<div class="prefs-page">

<h3>Log in to your account</h3>
<div class="prefs-box">
<div align="center">
<h4>Please anter your login and password</h4>
${h.form(h.url_for(action='submit'), method='post')}
Username: ${h.text_field('username')}<br/>
Password: ${h.password_field('password')}<br/>
				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
${h.end_form()}
</div>
</div>
</div>
