from gallery.tests import *

class TestSandboxController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='sandbox', action='index'))
        # Test response...
