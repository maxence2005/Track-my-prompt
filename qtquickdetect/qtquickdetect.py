import logging
import os
import pathlib
import sys
import shutil
import nltk

from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# from models.app_state import AppState
from .utils import filepaths
from .controller.backend import Backend
from .models.encylo import DatabaseManager
from .models.historique import DatabaseManagerHistorique
from .models.mediaModel import DatabaseManagerMedia
from .controller.ColorManager import ColorManager
from .controller.LanguageManager import LanguageManager
from .models.app_config import AppConfig


def main():
    # Get path to the python package
    package_path = pathlib.Path(__file__).absolute().parent.parent

    # Configure logging
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    # Create necessary directories
    filepaths.create_cache_dir()
    filepaths.create_config_dir()
    filepaths.create_data_dir()

    nltk_file = filepaths.get_base_cache_dir() / 'nltk.txt'

    if not os.path.exists(nltk_file):
        with open(nltk_file, 'w') as f:
            f.write("NLTK resources initialization.\n")
        nltk.download('wordnet')
        nltk.download('omw-1.4')

    os.environ['TORCH_HOME'] = str(filepaths.get_base_data_dir() / 'weights')

    # Change working directory to the package path
    os.chdir(package_path)
    print("Starting TrackMyPrompt") 
    db_path_tmp = os.path.abspath("qtquickdetect/resources/trackmyprompts.db")
    data_dir = filepaths.get_base_data_dir()
    db_path = os.path.join(data_dir, "trackmyprompt.db")

    if not os.path.exists(db_path):
        try:
            shutil.copy(db_path_tmp, db_path)
        except IOError as e:
            print(f"Erreur lors de la copie de la base de données : {e}")

    if not os.path.isfile(db_path):
        sys.exit(-1)

    try:
        database_manager = DatabaseManager(db_path)
        database_manager_historique = DatabaseManagerHistorique(db_path)

        database_media = DatabaseManagerMedia(db_path)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de DatabaseManager : {e}")
        sys.exit(-1)
    
    # Create an instance of QQmlApplicationEngine
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    language_manager = LanguageManager(app=app, engine=engine, encyclo=database_manager.encyclopediaModel)
    app_config = AppConfig(language_manager.languages)

    language_manager.setLanguage(app_config.language)
    theme = app_config.style
    ia_method = "dumb"
    api_key = ""
    
    media_model = database_media
    backend = Backend(media_model, database_media._media_model.rowCount(), ia_method, api_key)
    color_manager = ColorManager("qtquickdetect/resources/themes.json", theme)
    

    # Expose the backend to the QML context
    engine.rootContext().setContextProperty("mediaModel", database_media._media_model)
    engine.rootContext().setContextProperty("databaseManager", database_manager)
    engine.rootContext().setContextProperty("databaseManagerHistorique", database_manager_historique)
    engine.rootContext().setContextProperty("encyclopediaModel", database_manager.encyclopediaModel)
    engine.rootContext().setContextProperty("historiqueModel", database_manager_historique.historiqueModel)

    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("colorManager", color_manager)
    engine.rootContext().setContextProperty("languageManager", language_manager)

    # Load the QML file
    engine.load(QUrl("qtquickdetect/views/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    statut = app.exec()

    app_config.style = color_manager.current_theme
    app_config.language = language_manager.language
    app_config.save()
    sys.exit(statut)
    