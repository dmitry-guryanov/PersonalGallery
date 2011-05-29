<%inherit file="base.mako"/>

<%def name="head()">
</%def>
<%def name="header()">
</%def>

<%include file="header.mako"/>

<div class="prefs-page">

<h3>Add photos to album</h3>
<div class="prefs-box">
<h4>Select one or more images or zip archives</h4>
${h.form(url(album, "commitaddphoto"), multipart=True, method='post')}
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
<div>${h.submit('submit0', 'Submit')}</div>
${h.end_form()}

<h4><a id="addOne" href="javascript:addOne()">More Upload Boxes...</a></h4>

<script type="text/javascript">
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
