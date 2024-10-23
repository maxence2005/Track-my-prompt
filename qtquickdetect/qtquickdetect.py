import logging
import os
import pathlib

import sys
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from .models.app_state import AppState
from .utils import filepaths



def main():
    # get path to python package
    package_path = pathlib.Path(__file__).absolute().parent.parent

    # Configure logging
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    filepaths.create_cache_dir()
    filepaths.create_config_dir()
    filepaths.create_data_dir()

    # Set the environment variable for the torch home directory
    os.environ['TORCH_HOME'] = str(filepaths.get_base_data_dir() / 'weights')

    os.chdir(package_path)
    print("Starting QtQuickDetect")

    # Set up the QApplication
    # Créer une instance d'application Qt
    app = QApplication(sys.argv)

    # Créer une instance du backend
    #backend = Backend()

    # Créer une instance de QQmlApplicationEngine
    engine = QQmlApplicationEngine()

    # Exposer le backend au contexte QML
    #engine.rootContext().setContextProperty("backend", backend)

    # Charger le fichier QML
    engine.load(QUrl("qtquickdetect/views/App.qml"))

    # Vérifier si le fichier QML est chargé correctement
    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    sys.exit(app.exec())
