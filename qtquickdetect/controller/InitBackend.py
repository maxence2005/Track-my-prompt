from PySide6.QtCore import QObject, Property, QThread, Signal, QCoreApplication, Slot

class Controller(QObject):
    """
    Controller class to initialize and manage the backend components.
    """
    controller_loading_finished = Signal()
    
    def __init__(self, app, engine, frame_provider):
        super().__init__()
        self.app = app
        self.engine = engine
        self.frame_provider = frame_provider

    def start(self):
        """
        Start the initialization of the backend components.
        """
        import sys

        from .backend import Backend
        from ..models.encylo import DatabaseManager
        from ..models.historique import DatabaseManagerHistorique
        from ..models.mediaModel import DatabaseManagerMedia
        from .ColorManager import ColorManager
        from .LanguageManager import LanguageManager
        from ..models.app_config import AppConfig
        from ..utils import filepaths

        import os
        import shutil
        import nltk
        
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
            self._database_manager = DatabaseManager(db_path)
            self._database_manager_historique = DatabaseManagerHistorique(db_path)

            self._database_media = DatabaseManagerMedia(db_path)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de DatabaseManager : {e}")
            sys.exit(-1)
        
        # Creating the instance of QQmlApplicationEngine
        self._language_manager = LanguageManager(app=self.app, engine=self.engine, encyclo=self._database_manager.encyclopediaModel)
        self._app_config = AppConfig(self._language_manager.languages)
        self._language_manager.setLanguage(self._app_config.language)
        theme = self._app_config.style
        ia_method = self._app_config.prompt_interpreter
        api_key = self._app_config.api_key

        self._backend = Backend(self._database_media, self._database_media._media_model.rowCount(), self.frame_provider, ia_method, api_key, self._database_manager.encyclopediaModel)
        self._color_manager = ColorManager("qtquickdetect/resources/themes.json", theme)
        
        self._database_manager.moveToThread(QCoreApplication.instance().thread())
        self._database_manager_historique.moveToThread(QCoreApplication.instance().thread())
        self._database_media.moveToThread(QCoreApplication.instance().thread())
        self._language_manager.moveToThread(QCoreApplication.instance().thread())
        self._backend.moveToThread(QCoreApplication.instance().thread())
        self._color_manager.moveToThread(QCoreApplication.instance().thread())

        self.controller_loading_finished.emit()

    
class InitBackend(QObject):
    """
    InitBackend class to manage the loading of the backend components.
    """
    loading_finished = Signal() 
    isLoaded = False
    
    def __init__(self, app, engine, frame_provider):
        super().__init__()
        self.app = app
        self.engine = engine
        self.frame_provider = frame_provider
        
    def start_loading(self):
        """
        Start loading the backend components in a separate thread.
        """
        self.thread = QThread()
        self.controller = Controller(self.app, self.engine, self.frame_provider)
        self.controller.controller_loading_finished.connect(self.on_loading_finished)
        self.controller.moveToThread(self.thread)
        self.thread.started.connect(self.controller.start)
        self.thread.start()
        
    @Slot()
    def stop_loading(self):
        """
        Stop the loading thread.
        """
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
    
    def on_loading_finished(self):
        """
        Handle the completion of the loading process.
        """
        self.isLoaded = True
        self.loading_finished.emit()
        self.stop_loading()
    
    @Property(QObject, constant=True)
    def mediaModel(self):
        """
        Get the media model.

        Returns:
            QObject: The media model.
        """
        self.raiseIfNotLoaded()
        return self.controller._database_media._media_model
    
    @Property(QObject, constant=True)
    def encyclopediaModel(self):
        """
        Get the encyclopedia model.

        Returns:
            QObject: The encyclopedia model.
        """
        self.raiseIfNotLoaded()
        return self.controller._database_manager.encyclopediaModel
    
    @Property(QObject, constant=True)
    def historiqueModel(self):
        """
        Get the historique model.

        Returns:
            QObject: The historique model.
        """
        self.raiseIfNotLoaded()
        return self.controller._database_manager_historique.historiqueModel
    
    @Property(QObject, constant=True)
    def colorManager(self):
        """
        Get the color manager.

        Returns:
            QObject: The color manager.
        """
        self.raiseIfNotLoaded()
        return self.controller._color_manager
    
    @Property(QObject, constant=True)
    def languageManager(self):
        """
        Get the language manager.

        Returns:
            QObject: The language manager.
        """
        self.raiseIfNotLoaded()
        return self.controller._language_manager
    
    @Property(QObject, constant=True)
    def appConfig(self):
        """
        Get the app configuration.

        Returns:
            QObject: The app configuration.
        """
        self.raiseIfNotLoaded()
        return self.controller._app_config
    
    @Property(QObject, constant=True)
    def databaseManager(self):
        """
        Get the database manager.

        Returns:
            QObject: The database manager.
        """
        self.raiseIfNotLoaded()
        return self.controller._database_manager
    
    @Property(QObject, constant=True)
    def backend(self):
        """
        Get the backend instance.

        Returns:
            QObject: The backend instance.
        """
        self.raiseIfNotLoaded()
        return self.controller._backend

    def raiseIfNotLoaded(self):
        """
        Raise an exception if the backend is not loaded yet.
        """
        if not self.isLoaded:
            raise BackendNotLoadException("Backend not loaded yet")
        
class BackendNotLoadException(Exception):
    """
    Exception raised when the backend is not loaded yet.
    """
    pass