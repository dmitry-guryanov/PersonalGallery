<%inherit file="base.mako"/>
<%def name="head()">
</%def>
<%def name="header()">
</%def>
<%include file="header.mako"/>


<div class="prefs-page">

<h3>Log in to your account</h3>
<div class="prefs-box">
<div>
<h4>Please anter your login and password</h4>
${h.form(url(root.login, 'login'))}
Username: ${h.text('username')}<br/>
Password: ${h.password('password')}<br/>
				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
</div>
${h.end_form()}
</div>
</div>
</div>
