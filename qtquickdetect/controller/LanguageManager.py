from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property, QPropertyAnimation, QTranslator, QLocale
from PySide6.QtWidgets import QApplication, QFileDialog
from ..utils import filepaths
import shutil
from pathlib import Path
from ..models.encylo import EncyclopediaModel
import json
import zipfile

class LanguageManager(QObject):
    newLanguage = Signal()
    languageChanged = Signal()
    translator = QTranslator()

    languages = {
        "English": ""
    }
    
    def check_structure(self, path):
        good = True
        if path.exists() and path.is_dir():
            required_files = ["language.ts", "language.qm", "encyclopedia.json"]
            for file_name in required_files:
                file_path = path / file_name
                if not file_path.exists():
                    good = False
                    break
        else :
            good = False
        
        return good

    def __init__(self, app, engine, encyclo: EncyclopediaModel, language="en"):
        super().__init__()
        self.app = app
        self.engine = engine
        self.language = language
        self.encyclopedia = encyclo
        filepaths.create_data_dir()
        path = filepaths.get_base_data_dir() / "languages"
        if path.exists() and path.is_dir():
            for dir in path.iterdir():
                if dir.is_dir() and self.check_structure(dir):
                    self.languages[dir.stem] = str(dir)

    def load_json_encyclopedia(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @Property("QVariant", notify=newLanguage)
    def getLanguages(self):
        return list(self.languages.keys())

    @Slot(str)
    def setLanguage(self, language):
        if language:
            self.translator.load(self.languages[language] + "/language.qm")
            if language == "English":
                self.encyclopedia.restoreName()
            else:
                newEncyclopedia = self.load_json_encyclopedia(self.languages[language] + "/encyclopedia.json")
                self.encyclopedia.changeName(newEncyclopedia)
            self.app.installTranslator(self.translator)
            self.engine.retranslate()
        else:
            self.app.removeTranslator(self.translator)

    @Slot()
    def install_new_language(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter(
            "Track-My-Prompt Translation (*.tmpts)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                for file in selected_files:
                    if file:
                        with zipfile.ZipFile(file, 'r') as zip_ref:
                            extract_path = filepaths.get_base_data_dir() / "languages" / Path(file).stem
                            zip_ref.extractall(extract_path)
                            if self.check_structure(extract_path):
                                self.languages[Path(file).stem] = str(extract_path)
                            else:
                                shutil.rmtree(extract_path)
                self.newLanguage.emit()
