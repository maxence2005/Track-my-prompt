import unittest
from unittest.mock import MagicMock, patch
import importer

ColorManager = importer.load('ColorManager', 'controller', 'ColorManager.py')

class TestColorManager(unittest.TestCase):
    def setUp(self):
        self.theme_file = "test_theme.json"
        self.theme = "light"
        with patch('builtins.open', unittest.mock.mock_open(read_data='{"light": {}, "dark": {}}')):
            self.colorManager = ColorManager(self.theme_file, self.theme)

    def test_switchTheme(self):
        self.colorManager.switchTheme()
        self.assertEqual(self.colorManager.current_theme, "dark")
        self.colorManager.switchTheme()
        self.assertEqual(self.colorManager.current_theme, "light")

if __name__ == '__main__':
    unittest.main()