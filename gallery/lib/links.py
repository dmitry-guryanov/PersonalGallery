from gallery.models import get_root

class MyLink:
	def __init__(self, name, url):
		self.name = name
		self.url = url

def get_link(req, s):
	s = unicode(s, "utf-8")

	items = map(lambda x: x.strip(), s.split(','))
	url = req.resource_url(get_root()[items[0]], items[1])
	return MyLink(items[2], url)
