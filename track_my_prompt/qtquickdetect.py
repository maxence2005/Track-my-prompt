import logging
import os
import pathlib
import sys
import shutil

from PySide6.QtCore import QObject, Signal, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
# from models.app_state import AppState

from .models.imageProvider import ImageProvider
from .controller.InitBackend import InitBackend
from .utils import filepaths

def main():
    """
    Main function to start the TrackMyPrompt application.
    Configures logging, initializes the QApplication and QQmlApplicationEngine,
    sets up the ImageProvider, and loads the QML file.
    """
    base = "track_my_prompt"
    

    if sys.platform == 'win32':
        config_dir = filepaths.get_base_config_dir()
        os.makedirs(config_dir, exist_ok=True)

        target_ffmpeg = os.path.join(config_dir, "ffmpeg.exe")

        if not os.path.exists(target_ffmpeg):
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            shutil.copy(ffmpeg_path, target_ffmpeg)
            print(f"ffmpeg copié vers : {target_ffmpeg}")

        os.environ["PATH"] = str(config_dir) + os.pathsep + os.environ.get("PATH", "")
        
        
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
    filepaths.create_cache_dir()
    filepaths.create_config_dir()
    filepaths.create_data_dir()
    appContext = InitBackend(app, engine, frame_provider)

    # Expose the backend to the QML context
    engine.rootContext().setContextProperty("appContext", appContext)
    font_id = QFontDatabase.addApplicationFont(base + "/views/fonts/smothy.otf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        print(f"Police(s) disponible(s) : {font_families}")
    else:
        print("Erreur : impossible de charger la police.")
    
    app.aboutToQuit.connect(appContext.stop_loading)

    # Load the QML app file
    engine.load(QUrl(base + "/views/App.qml"))
    appContext.loading_finished.connect(lambda: engine.rootObjects()[0].setProperty("isLoaded", True))

    appContext.start_loading()

    if not engine.rootObjects():
        sys.exit(-1)

    icon_path = base + "/views/imgs/icon.png"
    icon = QIcon(icon_path)

    if icon.isNull():
        raise ValueError(f"Erreur : Impossible de charger l'icône depuis le chemin '{icon_path}'")
    else:
        app.setWindowIcon(icon)
    statut = app.exec()

    appContext.appConfig.style = appContext.colorManager.current_theme
    appContext.appConfig.language = appContext.languageManager.language
    appContext.appConfig.languages = appContext.languageManager.languages
    appContext.appConfig.prompt_interpreter = appContext.backend.shared_variable["prompt_ia"]
    appContext.appConfig.api_key = appContext.backend.shared_variable["api_key_mistral"]
    appContext.appConfig.frameManager = appContext.backend.shared_variable["frame_color"]
    appContext.appConfig.unlock_100 = appContext.backend.hasUnlocked100()
    appContext.appConfig.transcription_mode = appContext.backend.getTranscriptionMode()
    appContext.appConfig.save()
    sys.exit(statut)
