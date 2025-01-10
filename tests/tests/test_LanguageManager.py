import unittest
from unittest.mock import MagicMock, patch
import importer

LanguageManager = importer.load('LanguageManager', 'controller', 'LanguageManager.py')
EncyclopediaModel = importer.load('EncyclopediaModel', 'models', 'encylo.py')

class TestLanguageManager(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.engine = MagicMock()
        self.encyclo = MagicMock(spec=EncyclopediaModel)
        self.languageManager = LanguageManager(self.app, self.engine, self.encyclo)

    def test_check_structure(self):
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_path.is_dir.return_value = True
        mock_path.__truediv__.return_value.exists.return_value = True
        self.assertTrue(self.languageManager.check_structure(mock_path))

    def test_setLanguage(self):
        self.languageManager.languages = {"English": ""}
        self.languageManager.setLanguage("English")
        self.app.installTranslator.assert_called_once()
        self.engine.retranslate.assert_called_once()

if __name__ == '__main__':
    unittest.main()