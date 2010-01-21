<%inherit file="base.html"/>

<%def name="header()">
</%def>

<%include file="header.mako"/>

<div class="prefs-page">

<h3>Add photos to album</h3>
<div class="prefs-box">
<h4>Select one or more images or zip archives</h4>
${h.secure_form(url.current(action='photo_add_submit'), multipart=True)}
% for i in range(20):
<%   if i < 2:
     style = "'display: block'"
   else:
     style = "'display: none'"
%>
	<div id="filediv-${i}" style=${style}>
Upload file:      ${h.file('new_photo-%d' % i)}
Caption:          ${h.text('description-%d' % i)} <br />
	</div>

% endfor
                  ${h.submit('submit0', 'Submit')}
${h.end_form()}

<script type="text/javascript">
	document.write('<h4><a id="addOne" href="javascript:addOne()">More Upload Boxes...</a></h4>');
	var fileIndex = 1;

	function addOne() {
		var link = document.getElementById('addOne');
		link.blur();
		document.getElementById('filediv-' + ++fileIndex).style.display = 'block';
		if (fileIndex >= 20) {
		link.style.display = 'none';
		}
}
</script>

</div>
</div>
