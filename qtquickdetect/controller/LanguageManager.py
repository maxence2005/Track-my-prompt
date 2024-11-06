from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property, QPropertyAnimation, QTranslator, QLocale
from PySide6.QtWidgets import QApplication, QFileDialog
from ..utils import filepaths
import shutil
from pathlib import Path

class LanguageManager(QObject):
    newLanguage = Signal()
    languageChanged = Signal()
    translator = QTranslator()

    languages = {
        "English": ""
    }

    def __init__(self, app, engine, language="en"):
        super().__init__()
        self.app = app
        self.engine = engine
        self.language = language
        filepaths.create_data_dir()
        path = filepaths.get_base_data_dir() / "languages"
        if path.exists() and path.is_dir():
            for file in path.iterdir():
                if file.is_file():
                    if file.suffix == ".qm":
                        self.languages[file.stem] = str(file)

    @Property("QVariant", notify=newLanguage)
    def getLanguages(self):
        return list(self.languages.keys())

    @Slot(str)
    def setLanguage(self, language):
        if language:
            self.translator.load(self.languages[language])
            self.app.installTranslator(self.translator)
            self.engine.retranslate()
        else:
            self.app.removeTranslator(self.translator)

    @Slot()
    def install_new_language(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter(
            "Qm file (*.qm)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                for file in selected_files:
                    if file:
                        shutil.copy(file, filepaths.get_base_data_dir() / "languages")
                        file_path = Path(file)
                        self.languages[file_path.stem] = str(file_path)
                self.newLanguage.emit()
