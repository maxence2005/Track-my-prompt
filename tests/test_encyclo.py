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
module_name = 'qtquickdetect.models.encylo'
module_path = os.path.join(project_root, 'qtquickdetect', 'models', 'encylo.py')

# Vérification de l'existence du fichier module
if os.path.exists(module_path):
    try:
        # Importation dynamique du module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        encyclo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(encyclo)

        # Récupération des classes du module
        DatabaseManager = getattr(encyclo, 'DatabaseManager', None)
        EncyclopediaModel = getattr(encyclo, 'EncyclopediaModel', None)

        # Vérification de la présence des classes
        if not DatabaseManager or not EncyclopediaModel:
            raise AttributeError("Les classes DatabaseManager ou EncyclopediaModel n'ont pas été trouvées.")

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
def mock_model():
    """Fixture pour créer une instance d'EncyclopediaModel."""
    return EncyclopediaModel()

@pytest.fixture
def mock_db_path():
    """Fixture pour fournir un chemin de base de données temporaire."""
    return 'qtquickdetect/resources/trackmyprompts.db'

@pytest.fixture
def database_manager(mock_db_path):
    """Fixture pour créer une instance de DatabaseManager avec un chemin de base de données temporaire."""
    return DatabaseManager(mock_db_path)

# -------------------------------
# TESTS UNITAIRES
# -------------------------------

def test_model_initial_state(mock_model):
    """✅ Vérifiez l'état initial du modèle (doit être vide)."""
    assert mock_model.rowCount() == 0

def test_load_data_success(database_manager):
    """✅ Testez la méthode de chargement des données avec une base de données valide."""
    database_manager.load_data()
    assert database_manager.model.rowCount() > 0

def test_load_data_database_error():
    """❌ Simulez une erreur de base de données avec un chemin de base de données invalide."""
    # Spécifiez l'exception attendue et incluez l'instanciation de DatabaseManager dans le bloc
    with pytest.raises(sqlite3.OperationalError):
        # Créez l'objet DatabaseManager qui va immédiatement lever l'exception
        invalid_db_manager = DatabaseManager("/invalid/path/to/db")


def test_model_update_data(mock_model):
    """✅ Testez la mise à jour des données dans le modèle."""
    new_data = [{"englishName": "Test Name", "emoticon": ":)", "timeFound": "2024-11-06"}]
    mock_model.update_data(new_data)
    assert mock_model.rowCount() == 1
    assert mock_model.data(mock_model.index(0), mock_model.NameRole) == "Test Name"
