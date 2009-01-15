from gallery.tests import *

class TestAlbumController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='album'))
        # Test response...
