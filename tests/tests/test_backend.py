import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
from PySide6.QtTest import QSignalSpy
import importer

Backend = importer.load('Backend', 'controller', 'backend.py')
DatabaseManagerMedia = importer.load('DatabaseManagerMedia', 'models', 'mediaModel.py')
ImageProvider = importer.load('ImageProvider', 'models', 'imageProvider.py')

class TestBackend(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.media_model = MagicMock(spec=DatabaseManagerMedia)
        self.image_provider = MagicMock(spec=ImageProvider)
        self.backend = Backend(
            media_model=self.media_model,
            row=0,
            im_pro=self.image_provider,
            prompt_ia="mistral",
            api_key_mistral="fake_api_key",
            encyclopedia_model=MagicMock()
        )
    
    def test_initial_shared_variable(self):
        # Verify the initial values of shared variables
        self.assertIn("settingsMenuShowed", self.backend.shared_variable)
        self.assertFalse(self.backend.shared_variable["settingsMenuShowed"])
        self.assertTrue(self.backend.shared_variable["Menu"])

    def test_receive_prompt_empty(self):
        # Case: empty prompt
        spy = QSignalSpy(self.backend.infoSent)
        self.backend.receivePrompt("")
        self.assertEqual(spy.count(), 1) # Verify that a signal was emitted
        emitted_args = spy.at(0)  # Get the first emission
        self.assertEqual(emitted_args, ["no_data_saved"])

    def test_receive_prompt_with_valid_data(self):
        # Case: valid prompt
        self.backend.fichier = {"id": 1, "lien": "/path/to/file.jpg", "type": "image"}
        with patch.object(self.backend.pipeline, 'start_processing') as mock_pipeline:
            self.backend.receivePrompt("Describe this image")
            self.assertTrue(self.backend._shared_variable["Chargement"])
            mock_pipeline.assert_called_once_with(
                "/path/to/file.jpg", "image", "Describe this image", "mistral", "fake_api_key"
            )

    def test_receive_file_with_invalid_url(self):
        # Case: invalid URL
        with patch('utils.url_handler.is_url', return_value=False):
            with patch.object(self.backend, 'handle_file') as mock_handle_file:
                self.backend.receiveFile("file:///invalid/path")
                mock_handle_file.assert_called_once_with("/invalid/path")

    def test_receive_file_with_valid_url(self):
        # Case: valid URL
        with patch('utils.url_handler.is_url', return_value=True):
            with patch.object(self.backend, 'handle_url') as mock_handle_url:
                self.backend.receiveFile("http://example.com/file.jpg")
                mock_handle_url.assert_called_once_with("http://example.com/file.jpg")

    def test_toggle_menu(self):
        # Verify the toggling of the menu
        initial_state = self.backend.shared_variable["Menu"]
        self.backend.toggle_menu()
        self.assertNotEqual(self.backend.shared_variable["Menu"], initial_state)
        
    def test_untoggle_menu(self):
        # Verify the toggling of the menu
        self.test_toggle_menu()

    def test_signals_emitted(self):
        # Verify if signals are emitted
        spy = QSignalSpy(self.backend.sharedVariableChanged)
        self.backend.toggle_menu()
        self.assertEqual(spy.count(), 1)  # One signal was emitted

    def test_get_file_path(self):
        # Test for converting URLs to local paths
        if sys.platform == 'win32':
            self.assertEqual(self.backend.get_file_path("file:///C:/path/to/file"), "C:/path/to/file")
        else:
            self.assertEqual(self.backend.get_file_path("file:///home/user/file"), "/home/user/file")

    def test_handle_media_image(self):
        # Case: processing an image
        with patch('utils.filepaths.get_base_data_dir', return_value=Path("/data")):
            with patch('shutil.copy') as mock_copy:
                self.media_model.addMediaItem.return_value = 1
                self.backend.handle_media("/path/to/image.jpg")
                mock_copy.assert_called_once()
                self.assertEqual(self.backend.fichier["type"], "image")
                self.assertEqual(self.backend.fichier["id"], 1)

if __name__ == '__main__':
    unittest.main()