import unittest
import sqlite3
import importer
HistoriqueModel = importer.load('HistoriqueModel', 'models', 'historique.py')
DatabaseManagerHistorique = importer.load('DatabaseManagerHistorique', 'models', 'historique.py')

class TestHistorique(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_db_path = 'qtquickdetect/resources/trackmyprompts.db'
        cls.database_manager_historique = DatabaseManagerHistorique(cls.mock_db_path)
        cls.mock_historique_model = HistoriqueModel()

    def test_model_initial_state(self):
        """✅ Vérifiez l'état initial du modèle (doit être vide)."""
        self.assertEqual(self.mock_historique_model.rowCount(), 0)

    def test_load_historique_data_success(self):
        """✅ Testez la méthode de chargement des données avec une base de données valide."""
        self.database_manager_historique.load_historique_data()
        self.assertGreater(self.database_manager_historique.historique_model.rowCount(), 0)

    def test_load_historique_data_database_error(self):
        """❌ Simulez une erreur de base de données avec un chemin de base de données invalide."""
        with self.assertRaises(sqlite3.OperationalError):
            invalid_db_manager = DatabaseManagerHistorique("/invalid/path/to/db")
            invalid_db_manager.load_historique_data()

    def test_historique_model_update_data(self):
        """✅ Testez la mise à jour des données dans le modèle."""
        new_data = [{"prompt": "Test Prompt"}]
        self.mock_historique_model.update_data(new_data)
        self.assertEqual(self.mock_historique_model.rowCount(), 1)
        self.assertEqual(
            self.mock_historique_model.data(
                self.mock_historique_model.index(0), 
                self.mock_historique_model.PromptRole
            ), 
            "Test Prompt"
        )

if __name__ == '__main__':
    unittest.main()