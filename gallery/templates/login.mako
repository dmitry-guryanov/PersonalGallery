<%inherit file="base.html"/>
<%def name="header()">
</%def>

<div align="center">
<h2>Log in to your account</h2>

${h.form(h.url(action='submit'), method='post')}
Username: ${h.text_field('username')}<br/>
Password: ${h.password_field('password')}<br/>
				${h.submit('enter', 'Login')}
				${h.submit('cancel', 'Cancel')}
${h.end_form()}
</div>

