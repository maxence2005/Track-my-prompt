import sys
import os
import importlib.util
import pytest
import sqlite3

# -------------------------------
# CONFIGURATION DU CHEMIN DU PROJET
# -------------------------------

# Chemin racine du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ajouter le chemin racine à sys.path pour la découverte des modules
sys.path.insert(0, project_root)

# -------------------------------
# CHARGEMENT DU MODULE DYNAMIQUE
# -------------------------------

# Nom et chemin du module à importer
module_name = 'qtquickdetect.models.historique'
module_path = os.path.join(project_root, 'qtquickdetect', 'models', 'historique.py')

# Vérification de l'existence du fichier module
if os.path.exists(module_path):
    try:
        # Importation dynamique du module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        historique = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(historique)

        # Récupération des classes du module
        HistoriqueModel = getattr(historique, 'HistoriqueModel', None)
        DatabaseManagerHistorique = getattr(historique, 'DatabaseManagerHistorique', None)

        # Vérification de la présence des classes
        if not HistoriqueModel or not DatabaseManagerHistorique:
            raise AttributeError("Les classes HistoriqueModel ou DatabaseManagerHistorique n'ont pas été trouvées.")

        print("✅ Module chargé avec succès, et les classes sont accessibles.")
    except AttributeError as e:
        print(f"❌ Erreur : {e}")
        raise
else:
    print(f"❌ Le module {module_name} n'existe pas à l'emplacement {module_path}")

# -------------------------------
# FIXTURES PYTEST
# -------------------------------

@pytest.fixture
def mock_historique_model():
    """Fixture pour créer une instance d'HistoriqueModel."""
    return HistoriqueModel()

@pytest.fixture
def mock_db_path():
    """Fixture pour fournir un chemin de base de données temporaire."""
    return 'qtquickdetect/resources/trackmyprompts.db'

@pytest.fixture
def database_manager_historique(mock_db_path):
    """Fixture pour créer une instance de DatabaseManagerHistorique avec un chemin de base de données temporaire."""
    return DatabaseManagerHistorique(mock_db_path)

# -------------------------------
# TESTS UNITAIRES
# -------------------------------

def test_model_initial_state(mock_historique_model):
    """✅ Vérifiez l'état initial du modèle (doit être vide)."""
    assert mock_historique_model.rowCount() == 0

def test_load_historique_data_success(database_manager_historique):
    """✅ Testez la méthode de chargement des données avec une base de données valide."""
    database_manager_historique.load_historique_data()
    assert database_manager_historique.historique_model.rowCount() > 0

def test_load_historique_data_database_error():
    """❌ Simulez une erreur de base de données avec un chemin de base de données invalide."""
    with pytest.raises(sqlite3.OperationalError):
        invalid_db_manager = DatabaseManagerHistorique("/invalid/path/to/db")

def test_historique_model_update_data(mock_historique_model):
    """✅ Testez la mise à jour des données dans le modèle."""
    new_data = [{"prompt": "Test Prompt"}]
    mock_historique_model.update_data(new_data)
    assert mock_historique_model.rowCount() == 1
    assert mock_historique_model.data(mock_historique_model.index(0), mock_historique_model.PromptRole) == "Test Prompt"
