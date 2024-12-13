
import unittest
from unittest.mock import patch, MagicMock

import importer
promptFiltre = importer.load('promptFiltre', 'models', 'filtre.py')

class TestPromptFiltre(unittest.TestCase):
    def test_promptFiltre_dumb(self):
        result = promptFiltre("dog cat", "dumb")
        self.assertEqual(result, ["dog", "cat"])

    def test_promptFiltre_dumb_ts(self):
        result = promptFiltre("chien chat", "dumb_ts")
        self.assertEqual(result, ["dog", "cat"])

# TODO
"""     @patch('qtquickdetect.models.filtre.requests.post')
    def test_promptFiltre_mistral(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"choices": [{"message": {"content": '["dog", "cat"]'}}]}
        result = promptFiltre("dog cat", "mistral", api_key="test_key")
        self.assertEqual(result, ["dog", "cat"]) """

if __name__ == '__main__':
    unittest.main()