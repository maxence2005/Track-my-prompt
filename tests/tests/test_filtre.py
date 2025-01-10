import unittest
from unittest.mock import patch, MagicMock
import importer

import key

promptFiltre = importer.load('promptFiltre', 'models', 'filtre.py')

class TestPromptFiltre(unittest.TestCase):
    def test_promptFiltre_dumb(self):
        result = promptFiltre("dog cat", "dumb")
        self.assertEqual(result, ["dog", "cat"])

    def test_promptFiltre_dumb_ts(self):
        result = promptFiltre("chien chat", "dumb_ts")
        self.assertEqual(result, ["dog", "cat"])

    def test_promptFiltre_mistral(self):
        assert key.mistral_key != 'your_mistral_key', "You need to set your mistral key in tests/key.py"
        result = promptFiltre("Find all the dogs, as well as the cats. However, I don't want to find humans", "mistral", api_key=key.mistral_key)
        self.assertEqual(result, ["dog", "cat"])

if __name__ == '__main__':
    unittest.main()