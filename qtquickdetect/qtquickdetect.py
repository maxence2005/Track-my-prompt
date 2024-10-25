import logging
import os
import pathlib
import sys

from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# from models.app_state import AppState
from .utils import filepaths
from .controller.backend import Backend
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
    print("Starting QtQuickDetect")

    # Create an instance of the backend
    backend = Backend()
    color_manager = ColorManager("qtquickdetect/resources/themes.json", "dark")
    
    # Create an instance of QQmlApplicationEngine
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Expose the backend to the QML context
    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("colorManager", color_manager)

    # Load the QML file
    engine.load(QUrl("qtquickdetect/views/App.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    sys.exit(app.exec())
