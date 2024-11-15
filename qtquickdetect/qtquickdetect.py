import logging
import os
import pathlib
import sys

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# from models.app_state import AppState

from .models.imageProvider import ImageProvider
from .controller.InitBackend import InitBackend

def main():
    # Get path to the python package
    package_path = pathlib.Path(__file__).absolute().parent.parent
    os.chdir(package_path)
    print("Starting TrackMyPrompt")
    # Configure logging
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    frame_provider = ImageProvider()
    engine.addImageProvider("frameProvider", frame_provider)
    
    appContext = InitBackend(app, engine, frame_provider)

    # Expose the backend to the QML context
    engine.rootContext().setContextProperty("appContext", appContext)
    font_id = QFontDatabase.addApplicationFont("qtquickdetect/views/fonts/smothy.otf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Police(s) disponible(s) : {font_families}")
    else:
        print("Erreur : impossible de charger la police.")
    
    # Connecter la méthode stop_loading au signal aboutToQuit
    app.aboutToQuit.connect(appContext.stop_loading)

    # Load the QML file
    engine.load(QUrl("qtquickdetect/views/App.qml"))
    appContext.loading_finished.connect(lambda: engine.rootObjects()[0].setProperty("isLoaded", True))

    appContext.start_loading()

    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    statut = app.exec()

    appContext.appConfig.style = appContext.colorManager.current_theme
    appContext.appConfig.language = appContext.languageManager.language
    appContext.appConfig.prompt_interpreter = appContext.backend.shared_variable["prompt_ia"]
    appContext.appConfig.api_key = appContext.backend.shared_variable["api_key_mistral"]
    appContext.appConfig.save()
    sys.exit(statut)
