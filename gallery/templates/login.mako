<%inherit file="base.mako"/>
<%def name="header()">
</%def>
<%include file="header.mako"/>


<div class="prefs-page">

<h3>${_("Log in to your account")}</h3>
<div class="prefs-box">
<div>
<h4>${_("Please anter your login and password")}</h4>
${h.secure_form(url.current(action='submit'), method='post')}
<div>
${_("Username")}: ${h.text('username')}<br/>
${_("Password")}: ${h.password('password')}<br/>
				${h.submit('enter', _('Login'))}
				${h.submit('cancel', _('Cancel'))}
</div>
${h.end_form()}
</div>
</div>
</div>
