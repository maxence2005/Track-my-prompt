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
        # Mock des dépendances
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
        # Vérifie les valeurs initiales des variables partagées
        self.assertIn("settingsMenuShowed", self.backend.shared_variable)
        self.assertFalse(self.backend.shared_variable["settingsMenuShowed"])
        self.assertTrue(self.backend.shared_variable["Menu"])

    def test_receive_prompt_empty(self):
        # Cas : prompt vide
        spy = QSignalSpy(self.backend.infoSent)
        self.backend.receivePrompt("")
        self.assertEqual(spy.count(), 1) # Vérifie qu'un signal a été émis
        emitted_args = spy.at(0)  # Récupère la première émission
        self.assertEqual(emitted_args, ["no_data_saved"])

    def test_receive_prompt_with_valid_data(self):
        # Cas : prompt valide
        self.backend.fichier = {"id": 1, "lien": "/path/to/file.jpg", "type": "image"}
        with patch.object(self.backend.pipeline, 'start_processing') as mock_pipeline:
            self.backend.receivePrompt("Describe this image")
            self.assertTrue(self.backend._shared_variable["Chargement"])
            mock_pipeline.assert_called_once_with(
                "/path/to/file.jpg", "image", "Describe this image", "mistral", "fake_api_key"
            )

    def test_receive_file_with_invalid_url(self):
        # Cas : URL invalide
        with patch('utils.url_handler.is_url', return_value=False):
            with patch.object(self.backend, 'handle_file') as mock_handle_file:
                self.backend.receiveFile("file:///invalid/path")
                mock_handle_file.assert_called_once_with("/invalid/path")

    def test_receive_file_with_valid_url(self):
        # Cas : URL valide
        with patch('utils.url_handler.is_url', return_value=True):
            with patch.object(self.backend, 'handle_url') as mock_handle_url:
                self.backend.receiveFile("http://example.com/file.jpg")
                mock_handle_url.assert_called_once_with("http://example.com/file.jpg")

    def test_toggle_menu(self):
        # Vérifie le basculement du menu
        initial_state = self.backend.shared_variable["Menu"]
        self.backend.toggle_menu()
        self.assertNotEqual(self.backend.shared_variable["Menu"], initial_state)
        
    def test_untoggle_menu(self):
        # Vérifie le basculement du menu
        self.test_toggle_menu()

    def test_signals_emitted(self):
        # Vérifie si les signaux sont émis
        spy = QSignalSpy(self.backend.sharedVariableChanged)
        self.backend.toggle_menu()
        self.assertEqual(spy.count(), 1)  # Un signal a été émis

    def test_get_file_path(self):
        # Test pour la conversion des URLs en chemins locaux
        if sys.platform == 'win32':
            self.assertEqual(self.backend.get_file_path("file:///C:/path/to/file"), "C:/path/to/file")
        else:
            self.assertEqual(self.backend.get_file_path("file:///home/user/file"), "/home/user/file")

    def test_handle_media_image(self):
        # Cas : traitement d'une image
        with patch('utils.filepaths.get_base_data_dir', return_value=Path("/data")):
            with patch('shutil.copy') as mock_copy:
                self.media_model.addMediaItem.return_value = 1
                self.backend.handle_media("/path/to/image.jpg")
                mock_copy.assert_called_once()
                self.assertEqual(self.backend.fichier["type"], "image")
                self.assertEqual(self.backend.fichier["id"], 1)

if __name__ == '__main__':
    unittest.main()