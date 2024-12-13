import unittest
import sqlite3
import importer
DatabaseManager = importer.load('DatabaseManager', 'models', 'encylo.py')
EncyclopediaModel = importer.load('EncyclopediaModel', 'models', 'encylo.py')

# -------------------------------
# TESTS UNITAIRES
# -------------------------------

class TestEncyclopediaModel(unittest.TestCase):

    def setUp(self):
        """Configurez les objets nécessaires pour les tests."""
        self.mock_model = EncyclopediaModel()
        self.mock_db_path = '../qtquickdetect/resources/trackmyprompts.db'
        self.database_manager = DatabaseManager(self.mock_db_path)

    def test_model_initial_state(self):
        """✅ Vérifiez l'état initial du modèle (doit être vide)."""
        self.assertEqual(self.mock_model.rowCount(), 0)

    def test_load_data_success(self):
        """✅ Testez la méthode de chargement des données avec une base de données valide."""
        self.database_manager.load_data()
        self.assertGreater(self.database_manager.model.rowCount(), 0)

    def test_load_data_database_error(self):
        """❌ Simulez une erreur de base de données avec un chemin de base de données invalide."""
        with self.assertRaises(sqlite3.OperationalError):
            invalid_db_manager = DatabaseManager("/invalid/path/to/db")

    def test_model_update_data(self):
        """✅ Testez la mise à jour des données dans le modèle."""
        new_data = [{"englishName": "Test Name", "emoticon": ":)", "timeFound": "2024-11-06"}]
        self.mock_model.update_data(new_data)
        self.assertEqual(self.mock_model.rowCount(), 1)
        self.assertEqual(self.mock_model.data(self.mock_model.index(0), self.mock_model.NameRole), "Test Name")

if __name__ == '__main__':
    unittest.main()
