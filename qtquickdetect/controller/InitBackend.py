from PySide6.QtCore import QObject, Property, QThread, Signal, QCoreApplication

class Controller(QObject):
    controller_loading_finished = Signal()
    
    def __init__(self, app, engine):
        super().__init__()
        self.app = app
        self.engine = engine

    def start(self):
        # Useful imports with threading
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
        
        # Create an instance of QQmlApplicationEngine
        self._language_manager = LanguageManager(app=self.app, engine=self.engine, encyclo=self._database_manager.encyclopediaModel)
        self._app_config = AppConfig(self._language_manager.languages)
        self._language_manager.setLanguage(self._app_config.language)
        theme = self._app_config.style

        self._backend = Backend(self._database_media, self._database_media._media_model.rowCount())
        self._color_manager = ColorManager("qtquickdetect/resources/themes.json", theme)
        
        self._database_manager.moveToThread(QCoreApplication.instance().thread())
        self._database_manager_historique.moveToThread(QCoreApplication.instance().thread())
        self._database_media.moveToThread(QCoreApplication.instance().thread())
        self._language_manager.moveToThread(QCoreApplication.instance().thread())
        self._backend.moveToThread(QCoreApplication.instance().thread())
        self._color_manager.moveToThread(QCoreApplication.instance().thread())

        self.controller_loading_finished.emit()

    
class InitBackend(QObject):
    loading_finished = Signal()  # Signal pour indiquer que le chargement est terminé
    isLoaded = False
    
    def __init__(self, app, engine):
        super().__init__()
        self.app = app
        self.engine = engine
        
    def start_loading(self):
        # Démarrer un thread séparé pour simuler le chargement
        self.thread = QThread()
        self.controller = Controller(self.app, self.engine)
        self.controller.controller_loading_finished.connect(self.on_loading_finished)
        self.controller.moveToThread(self.thread)
        self.thread.started.connect(self.controller.start)
        self.thread.start()
    
    def on_loading_finished(self):
        self.isLoaded = True
        self.loading_finished.emit()
        self.thread.quit()
        self.thread.wait()
    
    @Property(QObject, constant=True)
    def mediaModel(self):
        self.raiseIfNotLoaded()
        return self.controller._database_media._media_model
    
    @Property(QObject, constant=True)
    def encyclopediaModel(self):
        self.raiseIfNotLoaded()
        return self.controller._database_manager.encyclopediaModel
    
    @Property(QObject, constant=True)
    def historiqueModel(self):
        self.raiseIfNotLoaded()
        return self.controller._database_manager_historique.historiqueModel
    
    @Property(QObject, constant=True)
    def colorManager(self):
        self.raiseIfNotLoaded()
        return self.controller._color_manager
    
    @Property(QObject, constant=True)
    def languageManager(self):
        self.raiseIfNotLoaded()
        return self.controller._language_manager
    
    @Property(QObject, constant=True)
    def appConfig(self):
        self.raiseIfNotLoaded()
        return self.controller._app_config
    
    @Property(QObject, constant=True)
    def databaseManager(self):
        self.raiseIfNotLoaded()
        return self.controller._database_manager
    
    @Property(QObject, constant=True)
    def backend(self):
        self.raiseIfNotLoaded()
        return self.controller._backend

    def raiseIfNotLoaded(self):
        if not self.isLoaded:
            raise Exception("Backend not loaded yet")