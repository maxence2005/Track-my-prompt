import unittest
import os
import sqlite3
from datetime import datetime
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import importer

DatabaseManager = importer.load('DatabaseManagerHistorique', 'models', 'historique.py')
HistoriqueModel = importer.load('HistoriqueModel', 'models', 'historique.py')

DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "../../track_my_prompt/resources/trackmyprompts.db"
))
class TestHistoriqueFonctionnalites(unittest.TestCase):

    def setUp(self):
        self.db_manager = DatabaseManager(DB_PATH)
        self.model = self.db_manager.historiqueModel
        self.test_pageID = 999999 

    def tearDown(self):
        self.db_manager.delete_by_pageID(self.test_pageID)

    def test_EX1_T1_affichage_historique_nominal_1(self):
        """EX1-T1 - Ajout d'un élément historique après un traitement"""
        data = {
            "id": -1,
            "pageID": self.test_pageID,
            "date_creation": datetime.now().strftime('%Y-%m-%d'),
            "lien": "image.jpg",
            "type": "image",
            "prompt": "Prompt test",
            "lienIA": "result_ia.jpg",
            "titre_case": "Cas Test"
        }
        self.model.add_item(data)
        self.assertTrue(self.model.has_pageID(self.test_pageID))

    def test_EX1_T2_ajout_multiples(self):
        """EX1-T2 - Ajout de plusieurs éléments, ordre respecté"""
        for i in range(3):
            data = {
                "id": -i,
                "pageID": self.test_pageID + i,
                "date_creation": datetime.now().strftime('%Y-%m-%d'),
                "lien": f"img_{i}.jpg",
                "type": "image",
                "prompt": f"Prompt {i}",
                "lienIA": f"result_ia_{i}.jpg",
                "titre_case": f"Titre {i}"
            }
            self.model.add_item(data)
        self.assertGreaterEqual(self.model.rowCount(), 3)

    def test_EX1_T3_modif_pendant_traitement(self):
        """EX1-T3 - Simulation de blocage pendant traitement"""
        self.db_manager._internal_pageID = self.test_pageID
        self.db_manager._shared_variable = {"Chargement": True}

        try:
            self.db_manager.delete_by_pageID(self.test_pageID)
        except Exception as e:
            self.fail(f"La suppression a levé une exception alors qu'elle devait être silencieusement bloquée : {e}")


    def test_EX1_T4_click_rapide(self):
        """EX1-T4 - Clique rapide sur un élément (pas de duplication)"""
        data = {
            "id": 1,
            "pageID": self.test_pageID,
            "date_creation": datetime.now().strftime('%Y-%m-%d'),
            "lien": "image.jpg",
            "type": "image",
            "prompt": "Prompt test",
            "lienIA": "result_ia.jpg",
            "titre_case": "Cas Test"
        }
        self.model.add_item(data)
        self.model.add_item(data)  
        count = sum(1 for item in self.model._items if item['pageID'] == self.test_pageID)
        self.assertEqual(count, 1)

    def test_EX1_T5_affichage_limite(self):
        """EX1-T5 - Ajout massif dans l'historique (>50)"""
        for i in range(51):
            self.model.add_item({
                "id": i,
                "pageID": self.test_pageID + i,
                "date_creation": "2025-01-01",
                "lien": f"img_{i}.jpg",
                "type": "image",
                "prompt": f"Prompt {i}",
                "lienIA": f"ia_{i}.jpg",
                "titre_case": f"Titre {i}"
            })
        self.assertGreaterEqual(self.model.rowCount(), 50)

    def test_EX2_T1_modif_prompt(self):
        """EX2-T1 - Modifier prompt existant"""
        self.model.add_item({
            "id": 101,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "a.jpg",
            "type": "image",
            "prompt": "Old Prompt",
            "lienIA": "ia.jpg",
            "titre_case": "Titre"
        })
        self.db_manager.update_items_by_pageID(self.test_pageID, "New Prompt")
        updated = next(item for item in self.model._items if item["pageID"] == self.test_pageID)
        self.assertEqual(updated["titre_case"], "New Prompt")

    def test_EX2_T3_prompt_vide(self):
        """EX2-T3 - Rejet modification si prompt vide"""
        self.model.add_item({
            "id": 102,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "a.jpg",
            "type": "image",
            "prompt": "Original",
            "lienIA": "ia.jpg",
            "titre_case": "Titre"
        })
        self.db_manager.update_items_by_pageID(self.test_pageID, "")
        updated = next(item for item in self.model._items if item["pageID"] == self.test_pageID)
        self.assertEqual(updated["prompt"], "Original")

    def test_EX2_T5_prompt_100_caracteres(self):
        """EX2-T5 - Prompt de 100 caractères"""
        prompt_long = "a" * 100
        self.model.add_item({
            "id": 103,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "a.jpg",
            "type": "image",
            "prompt": "short",
            "lienIA": "ia.jpg",
            "titre_case": "Titre"
        })
        self.db_manager.update_items_by_pageID(self.test_pageID, prompt_long)
        updated = next(item for item in self.model._items if item["pageID"] == self.test_pageID)
        self.assertEqual(updated["titre_case"], prompt_long)

    def test_EX3_T1_suppression_nominale(self):
        """EX3-T1 - Suppression simple d’un élément"""
        self.model.add_item({
            "id": 200,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "img.jpg",
            "type": "image",
            "prompt": "à supprimer",
            "lienIA": "ia.jpg",
            "titre_case": "test"
        })
        self.db_manager.delete_by_pageID(self.test_pageID)
        self.db_manager.remove_items_from_model(self.test_pageID)
        self.assertFalse(self.model.has_pageID(self.test_pageID))

    def test_EX3_T2_suppression_second_element(self):
        """EX3-T2 - Suppression d’un second élément"""
        for i in range(2):
            pid = self.test_pageID + i
            self.model.add_item({
                "id": 201 + i,
                "pageID": pid,
                "date_creation": "2025-01-01",
                "lien": f"{i}.jpg",
                "type": "image",
                "prompt": f"prompt {i}",
                "lienIA": f"ia_{i}.jpg",
                "titre_case": "test"
            })
        self.db_manager.delete_by_pageID(self.test_pageID + 1)
        self.db_manager.remove_items_from_model(self.test_pageID + 1)
        self.assertFalse(self.model.has_pageID(self.test_pageID + 1))
        self.assertTrue(self.model.has_pageID(self.test_pageID))

    def test_EX3_T3_suppression_en_detection(self):
        """EX3-T3 - Suppression bloquée pendant détection"""
        self.db_manager._internal_pageID = self.test_pageID
        self.db_manager._shared_variable = {"Chargement": True}
        self.model.add_item({
            "id": 203,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "img.jpg",
            "type": "image",
            "prompt": "à bloquer",
            "lienIA": "ia.jpg",
            "titre_case": "test"
        })
        try:
            self.db_manager.delete_by_pageID(self.test_pageID)
            self.db_manager.remove_items_from_model(self.test_pageID)

        except Exception:
            self.fail("Suppression multiple rapide a causé une erreur")

    def test_EX3_T4_suppression_rapide(self):
        """EX3-T4 - Double suppression rapide d’un même élément"""
        self.model.add_item({
            "id": 204,
            "pageID": self.test_pageID,
            "date_creation": "2025-01-01",
            "lien": "img.jpg",
            "type": "image",
            "prompt": "duplicat",
            "lienIA": "ia.jpg",
            "titre_case": "test"
        })
        self.db_manager.delete_by_pageID(self.test_pageID)
        self.db_manager.remove_items_from_model(self.test_pageID)

        try:
            self.db_manager.delete_by_pageID(self.test_pageID)
            self.db_manager.remove_items_from_model(self.test_pageID)

        except Exception:
            self.fail("Suppression multiple rapide a causé une erreur")

    def test_EX3_T5_suppression_massive(self):
        """EX3-T5 - Suppression de masse"""
        for i in range(50):
            self.model.add_item({
                "id": 300 + i,
                "pageID": self.test_pageID + i,
                "date_creation": "2025-01-01",
                "lien": f"{i}.jpg",
                "type": "image",
                "prompt": f"bulk {i}",
                "lienIA": f"bulk_ia_{i}.jpg",
                "titre_case": f"Bulk {i}"
            })
        for i in range(50):
            self.db_manager.delete_by_pageID(self.test_pageID + i)
            self.db_manager.remove_items_from_model(self.test_pageID + i)

        count = sum(1 for item in self.model._items if item['pageID'] >= self.test_pageID)
        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()
