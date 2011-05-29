from gallery.tests import *

class TestPhotoController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='photo'))
        # Test response...
