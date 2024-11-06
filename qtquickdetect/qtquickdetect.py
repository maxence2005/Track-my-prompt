import logging
import os
import pathlib
import sys
import shutil

from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# from models.app_state import AppState
from .utils import filepaths
from .controller.backend import Backend
from .models.encylo import DatabaseManager
from .models.mediaModel import DatabaseManagerMedia
from .controller.ColorManager import ColorManager


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

    # Set the environment variable for the torch home directory
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
    else:
        print("Le fichier trackmyprompt.db existe déjà dans le dossier de données.")

    if not os.path.isfile(db_path):
        sys.exit(-1)

    try:
        database_manager = DatabaseManager(db_path)
        database_media = DatabaseManagerMedia(db_path)
    except Exception as e:
        print(f"Erreur lors de l'initialisation de DatabaseManager : {e}")
        sys.exit(-1)
        
    theme = "dark"

    media_model = database_media
    backend = Backend(media_model, database_media._media_model.rowCount())
    color_manager = ColorManager("qtquickdetect/resources/themes.json", theme)
    

    # Create an instance of QQmlApplicationEngine
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    engine.rootContext().setContextProperty("mediaModel", database_media._media_model)

    engine.rootContext().setContextProperty("databaseManager", database_manager)

    engine.rootContext().setContextProperty("encyclopediaModel", database_manager.encyclopediaModel)
    # Expose the backend to the QML context
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("colorManager", color_manager)

    # Load the QML file
    engine.load(QUrl("qtquickdetect/views/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    sys.exit(app.exec())
