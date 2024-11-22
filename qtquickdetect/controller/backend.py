import sys
import os
import shutil
from urllib.parse import urlparse
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, QUrl, Property
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtQml import QQmlApplicationEngine


sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.imageProvider import ImageProvider
from utils.file_explorer import open_file_explorer
from utils.filepaths import get_base_config_dir, get_base_data_dir, create_config_dir, create_data_dir
from utils.url_handler import is_image, is_video, is_live_video, is_url, download_file
from pipeline.pipelinePrompt import PipelinePrompt
from pipeline.pipelineCamera import CameraPipeline
from models.mediaModel import DatabaseManagerMedia

class Backend(QObject):

    infoSent = Signal(str)
    promptEnter = Signal(str)
    sharedVariableChanged = Signal()
    idChargementSignal = Signal()


    def __init__(self, media_model: DatabaseManagerMedia, row, im_pro: ImageProvider, prompt_ia, api_key_mistral, encyclopedia_model):
        super().__init__()
        self.media_model = media_model
        self.encyclo_model = encyclopedia_model
        self.image_provider = im_pro
        self._shared_variable = {"settingsMenuShowed": False, "Erreur": False, "Menu": True, "Chargement" : False, "prompt_ia" : prompt_ia, "api_key_mistral" : api_key_mistral, "Camera" : False}
        self.pipeline = PipelinePrompt(self, encyclo_model=self.encyclo_model)
        self.pipelineCamera = CameraPipeline(self)
        self.pipelineCamera.frame_send.connect(self.frame_send)

        if row == 0:
            self._shared_variable["Start"] = True
            self.start = True
            self.fichier = {"id": -1, "lien" : "", "type" : ""}
            self._idChargement = None
        else :
            self._shared_variable["Start"] = False
            self.start = False
            tmp = self.media_model.get_last_media()
            self.fichier = {"id": tmp["id"], "lien" : tmp["lien"], "type" : tmp["type"]}
            self._idChargement = tmp["id"]
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

    @Property('QVariant', notify=idChargementSignal)
    def idChargement(self):
        return self._idChargement
    
    @Slot(str)
    def receivePrompt(self, promptText):
        if self.fichier["lien"] == "" :
            self.infoSent.emit("Erreur : Aucune Image/video enregistrer.")
        if self._shared_variable["prompt_ia"] == "mistral" and self._shared_variable["api_key_mistral"] == "":
            self.infoSent.emit("Erreur : Veuillez renseigner une clé API pour Mistral.")
        else :
            if promptText != "":
                self._shared_variable["Chargement"] = True
                self._idChargement = self.fichier["id"]
                self.sharedVariableChanged.emit()
                self.idChargementSignal.emit()
                self.pipeline.start_processing(self.fichier["lien"], self.fichier["type"], promptText, self._shared_variable["prompt_ia"], self._shared_variable["api_key_mistral"])
    
    @Slot(str, str)
    def change_prompt_recognition(self, prompt_ia, api_key_mistral = ""):
        self._shared_variable["prompt_ia"] = prompt_ia
        self._shared_variable["api_key_mistral"] = api_key_mistral
        self.sharedVariableChanged.emit()
    
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

    def on_processing_complete(self, result, promptText):
        self.media_model.updateMediaItem(id=self.fichier["id"], file_path_ia=result, prompt=promptText)
        self._shared_variable["Chargement"] = False
        self.sharedVariableChanged.emit()

    def get_file_path(self, fileUrl):
        if fileUrl.startswith("file:///"):
            if sys.platform == 'win32':
                return fileUrl[8:]
            elif sys.platform == 'darwin':
                raise Exception('macOS is not supported yet')
            else:
                return fileUrl[7:]
        return fileUrl
    
    def handle_media(self, file_path, is_url=False):
        if is_url:
            parsed_url = urlparse(file_path)
            filename = os.path.basename(parsed_url.path)
        else:
            filename = os.path.basename(file_path)
        
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            destination_directory = get_base_data_dir() / "collections" / "image"
            media_type = "image"
        elif file_extension in ['.mp4', '.avi', '.mkv', '.mov']:
            destination_directory = get_base_data_dir() / "collections" / "video"
            media_type = "video"
        else:
            self.infoSent.emit(f"Erreur : le fichier n'est pas une image ou une vidéo.")
            return
        
        dst = destination_directory / filename
        
        try:
            if is_url:
                download_file(file_path, dst)
            else:
                shutil.copy(file_path, dst)
            
            self.fichier["lien"] = str(dst)
            self.fichier["type"] = media_type
            id_row = self.media_model.addMediaItem(str(dst), media_type)
            self.fichier["id"] = id_row
        except Exception as e:
            self.infoSent.emit(f"Erreur : {e}")
    
    def handle_url(self, file_path):
        self.handle_media(file_path, is_url=True)
    
    def handle_file(self, file_path):
        self.handle_media(file_path, is_url=False)

    @Slot()
    def start_Camera(self):
        self.pipelineCamera.start_camera_recording()

    @Slot()
    def stop_Camera(self):
        self.pipelineCamera.stop_camera_recording()
    
    def on_recording_complete(self, lien):
        self.fichier["lien"] = str(lien)
        self.fichier["type"] = 'video'
        if self.start == True :
            self.start = False
            self._shared_variable["Start"] = False
            self.sharedVariableChanged.emit()
        id_row = self.media_model.addMediaItem(str(lien), 'video')
        self.fichier["id"] = id_row


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
                for file in selected_files:
                    self.receiveFile(file)
    @Slot()
    def toggle_menu(self):
        self._shared_variable["Menu"] = not self._shared_variable["Menu"]
        self.sharedVariableChanged.emit()
        
    @Slot()
    def toggle_erreur(self):
        self._shared_variable["Erreur"] = not self._shared_variable["Erreur"]
        self.sharedVariableChanged.emit()

    @Slot()
    def toggle_camera(self):
        self._shared_variable["Camera"] = not self._shared_variable["Camera"]
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
        
    @Property(str, notify=sharedVariableChanged)
    def getSizeOfHistory(self):
        image_dir = get_base_data_dir() / "collections" / "image"
        video_dir = get_base_data_dir() / "collections" / "video"
        image_value = sum(f.stat().st_size for f in image_dir.glob('**/*') if f.is_file())
        video_value = sum(f.stat().st_size for f in video_dir.glob('**/*') if f.is_file())
        total_size = image_value + video_value
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if total_size < 1024.0 or unit == 'TB':
                return f"{total_size:.2f} {unit}"
            total_size /= 1024.0
    
    @Slot()
    def deleteHistory(self):
        self.nouvelleDetection()
        image_dir = get_base_data_dir() / "collections" / "image"
        video_dir = get_base_data_dir() / "collections" / "video"
        def delete_files(directory):
            for file in directory.glob('**/*'):
                if file.is_file():
                    file.unlink()
                if file.is_dir():
                    shutil.rmtree(file)
        delete_files(image_dir)
        delete_files(video_dir)
        self.sharedVariableChanged.emit()
    
    def frame_send(self, frame):
        self.image_provider.set_image(frame)
