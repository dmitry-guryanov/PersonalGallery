<%inherit file="base.html"/>

<%def name="header()">
</%def>


${h.form(h.url(action='add_photo_submit'), multipart=True)}
Upload file:      ${h.file_field('new_photo')} <br />
File description: ${h.text_field('description')} <br />
                  ${h.submit('Submit')}
${h.end_form()}
