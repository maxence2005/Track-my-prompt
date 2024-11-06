import sys
import os
import shutil
from urllib.parse import urlparse
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, QUrl, Property
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtQml import QQmlApplicationEngine

sys.path.append(str(Path(__file__).resolve().parent.parent))


from utils.file_explorer import open_file_explorer
from utils.filepaths import get_base_config_dir, get_base_data_dir, create_config_dir, create_data_dir
from utils.url_handler import is_image, is_video, is_live_video, is_url, download_file

class Backend(QObject):

    infoSent = Signal(str)
    promptEnter = Signal(str)
    sharedVariableChanged = Signal()


    def __init__(self, media_model, row):
        super().__init__()
        self.media_model = media_model
        if row == 0:
            self._shared_variable = {"settingsMenuShowed": False, "Erreur": False, "Menu": True, "Start": True}
            self.start = True
            self.fichier = {"lien" : "", "type" : ""}
        else :
            self._shared_variable = {"settingsMenuShowed": False, "Erreur": False, "Menu": True, "Start": False}
            self.start = False
            tmp = self.media_model.get_last_media()
            self.fichier = {"lien" : tmp["lien"], "type" : tmp["type"]}
        create_config_dir()
        create_data_dir()

    @Property('QVariant', notify=sharedVariableChanged)
    def shared_variable(self):
        return self._shared_variable

    @shared_variable.setter
    def shared_variable(self, value):
        if self._shared_variable != value:
            self._shared_variable = value
            self.sharedVariableChanged.emit()

    @Slot(str)
    def receivePrompt(self, promptText):
        if self.fichier["lien"] == "" :
            self.infoSent.emit(f"Erreur : Aucune Image/video enregistrer.")
        else :
            if promptText != "":
                self.media_model.addMediaItem(self.fichier["lien"], self.fichier["type"], promptText)
    
    @Slot(str)
    def receiveFile(self, fileUrl):
        file_path = self.get_file_path(fileUrl)
        if self.start == True :
            self.start = False
            self._shared_variable["Start"] = False
            self.sharedVariableChanged.emit()
            
        if is_url(file_path):
            self.handle_url(file_path)
        else:
            self.handle_file(file_path)

    
    def get_file_path(self, fileUrl):
        if fileUrl.startswith("file:///"):
            if sys.platform == 'win32':
                return fileUrl[8:]
            elif sys.platform == 'darwin':
                raise Exception('macOS is not supported yet')
            else:
                return fileUrl[7:]
        return fileUrl
    
    def handle_url(self, file_path):
        if is_image(file_path):
            destination_directory = get_base_data_dir() / "collections" / "image"
            media_type = "image"
        elif is_video(file_path) or is_live_video(file_path):
            destination_directory = get_base_data_dir() / "collections" / "video"
            media_type = "video"
        elif is_live_video(file_path):
            destination_directory = get_base_data_dir() / "collections" / "video"
            media_type = "video"
        else:
            self.infoSent.emit(f"Erreur : l'url n'est pas une image ou une vidéo.")
            return
    
        parsed_url = urlparse(file_path)
        filename = os.path.basename(parsed_url.path)
        dst = destination_directory / filename
        download_file(file_path, dst)
        self.fichier["lien"] = str(dst)
        self.fichier["type"] = media_type
        self.media_model.addMediaItem(str(dst), media_type, "")
    
    def handle_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            destination_directory = get_base_data_dir() / "collections" / "image"
            media_type = "image"
        elif file_extension in ['.mp4', '.avi', '.mkv', '.mov']:
            destination_directory = get_base_data_dir() / "collections" / "video"
            media_type = "video"
        else:
            self.infoSent.emit(f"Erreur : le fichier n'est pas une image ou une vidéo.")
            return
    
        try:
            shutil.copy(file_path, destination_directory)

            self.media_model.addMediaItem(str(destination_directory / os.path.basename(file_path)), media_type, "")
            self.fichier["lien"] = str(destination_directory / os.path.basename(file_path))
            self.fichier["type"] = media_type
        except Exception as e:
            self.infoSent.emit(f"Erreur : {e}")

    @Slot()
    def selectFile(self):
        try:
            destination_directory = get_base_data_dir() / "collections"
            os.makedirs(destination_directory, exist_ok=True)
            open_file_explorer(destination_directory)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de l'explorateur de fichiers : {e}")
            self.infoSent.emit(f"Erreur : {e}")

    @Slot()
    def openFileExplorer(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images et vidéos (*.jpg *.jpeg *.png *.gif *.bmp *.mp4 *.avi *.mov *.mkv)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.receiveFile(selected_files[0])
    @Slot()
    def toggle_menu(self):
        self._shared_variable["Menu"] = not self._shared_variable["Menu"]
        self.sharedVariableChanged.emit()
        
    @Slot()
    def toggle_erreur(self):
        self._shared_variable["Erreur"] = not self._shared_variable["Erreur"]
        self.sharedVariableChanged.emit()

    @Slot()
    def toggle_param(self):
        self._shared_variable["settingsMenuShowed"] = not self._shared_variable["settingsMenuShowed"]
        self.sharedVariableChanged.emit()

    @Slot()
    def nouvelleDetection(self):
        self.media_model.clear_all_media()
        if self.start == False :
            self.start = True
            self._shared_variable["Start"] = True
            self.sharedVariableChanged.emit()
        self.fichier = {"lien" : "", "type" : ""}
