from gallery.tests import *

class TestAlbumEditController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='album_edit'))
        # Test response...
