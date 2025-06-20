import sys
import os
import shutil
import sqlite3
from urllib.parse import urlparse
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, QUrl, Property
from PySide6.QtWidgets import QApplication, QFileDialog, QColorDialog
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QImage, QColor

sys.path.append(str(Path(__file__).resolve().parent.parent))

from models.imageProvider import ImageProvider
from utils.file_explorer import open_file_explorer
from utils.filepaths import get_base_config_dir, get_base_data_dir, create_config_dir, create_data_dir
from utils.url_handler import is_image, is_video, is_live_video, is_url, download_file
from pipeline.pipelinePrompt import PipelinePrompt
from pipeline.pipelineCamera import CameraPipeline
from models.mediaModel import DatabaseManagerMedia
from models.transcripteur_vocal import AudioRecorder

class Backend(QObject):

    infoSent = Signal(str)
    promptEnter = Signal(str)
    sharedVariableChanged = Signal()
    idChargementSignal = Signal()
    celebrationUnlocked = Signal()

    def __init__(self, media_model: DatabaseManagerMedia, row: int, db_path: str, historique_model: QObject, im_pro: ImageProvider, prompt_ia: str, api_key_mistral: str, frame_color: str, unlock_100: bool, encyclopedia_model: QObject):
        """
        Initialize the Backend with the given parameters.

        Args:
            media_model (DatabaseManagerMedia): The media model instance.
            row (int): The row count.
            im_pro (ImageProvider): The image provider instance.
            prompt_ia (str): The prompt interpreter method.
            api_key_mistral (str): The API key for Mistral.
            encyclopedia_model (QObject): The encyclopedia model instance.
        """
        super().__init__()
        self._internal_pageID = 0
        self.media_model = media_model
        self.historique_model = historique_model
        self.db_path = db_path
        self.encyclo_model = encyclopedia_model
        self.image_provider = im_pro
        self._has_unlocked_100 = unlock_100
        self._shared_variable = {"settingsMenuShowed": False, "Erreur": False, "Menu": True, "Chargement" : False, "prompt_ia" : prompt_ia, "api_key_mistral" : api_key_mistral, "Camera" : False, "state" : "", "frame_color": frame_color}
        self.pipeline = PipelinePrompt(self, encyclo_model=self.encyclo_model)
        self.pipelineCamera = CameraPipeline(self)
        self.pipelineCamera.frame_send.connect(self.frame_send)
        self.audio_recorder = AudioRecorder()

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

    @Property(int)
    def current_pageID(self):
        return self._internal_pageID

    @Property('QVariant', notify=sharedVariableChanged)
    def shared_variable(self) -> dict:
        """
        Get the shared variable.

        Returns:
            dict: The shared variable.
        """
        return self._shared_variable

    @shared_variable.setter
    def shared_variable(self, value: dict):
        """
        Set the shared variable.

        Args:
            value (dict): The new value for the shared variable.
        """
        if self._shared_variable != value:
            self._shared_variable = value
            self.sharedVariableChanged.emit()

    @Property('QVariant', notify=idChargementSignal)
    def idChargement(self) -> int:
        """
        Get the ID of the current loading process.

        Returns:
            int: The ID of the current loading process.
        """
        return self._idChargement
    
    @Slot(str)
    def receivePrompt(self, promptText: str):
        """
        Receive a prompt text and start processing.

        Args:
            promptText (str): The prompt text.
        """
        if self.fichier["lien"] == "" :
            self.infoSent.emit("no_data_saved")
        elif self._shared_variable["prompt_ia"] == "mistral" and self._shared_variable["api_key_mistral"] == "":
            self.infoSent.emit("missing_mistral_api_key")
        else :
            if promptText != "" and self._shared_variable["Chargement"] == False:
                self._shared_variable["Chargement"] = True
                self._shared_variable["state"] = "prompt"
                self._idChargement = self.fichier["id"]
                self.sharedVariableChanged.emit()
                self.idChargementSignal.emit()
                id = self.add_to_historique(promptText, self.fichier["lien"], self.fichier["type"], "")
                print(f"voici l'id dans receivePrompt : {id}")
                self.pipeline.start_processing(self.fichier["lien"], self.fichier["type"], promptText, self._shared_variable["prompt_ia"], self._shared_variable["api_key_mistral"],id)

    @Slot(str, str)
    def change_prompt_recognition(self, prompt_ia: str, api_key_mistral: str = ""):
        """
        Change the prompt recognition method and API key.

        Args:
            prompt_ia (str): The prompt interpreter method.
            api_key_mistral (str, optional): The API key for Mistral. Defaults to "".
        """
        self._shared_variable["prompt_ia"] = prompt_ia
        self._shared_variable["api_key_mistral"] = api_key_mistral
        self.sharedVariableChanged.emit()

    @Slot(str)
    def setFrameManagerColor(self, hex_color):
        self._shared_variable["frame_color"] = hex_color
        self.sharedVariableChanged.emit()
    
    @Slot()
    def toggle_rainbow(self):
        self._shared_variable["frame_color"] = "rainbow"
        self.sharedVariableChanged.emit()

    @Slot()
    def disable_rainbow(self):
        self._shared_variable["frame_color"] = "#00FF00"
        self.sharedVariableChanged.emit()

    @Slot()
    def openColorDialog(self):
        color = QColorDialog.getColor(
            initial=QColor(self._shared_variable["frame_color"]),
            options=QColorDialog.ColorDialogOption.ShowAlphaChannel
        )

        if color.isValid():
            hex_color = color.name() 
            self._shared_variable["frame_color"] = hex_color
            self.sharedVariableChanged.emit()
    @Slot()
    def startOnFalse(self):
        self.start = False
        self._shared_variable["Start"] = False
        self.sharedVariableChanged.emit()
    
    @Slot(str)
    def receiveFile(self, fileUrl: str):
        """
        Receive a file URL and handle the file.

        Args:
            fileUrl (str): The file URL.
        """
        file_path = self.get_file_path(fileUrl)
            
        if is_url(file_path):
            self.handle_url(file_path)
        else:
            self.handle_file(file_path)

    def on_processing_complete(self, result: str, promptText: str, idElem):
        """
        Handle the completion of the processing.

        Args:
            result (str): The result of the processing.
            promptText (str): The prompt text.
        """
        
        if result:
            self.media_model.updateMediaItem(id=self.fichier["id"], file_path_ia=result, prompt=promptText)
            self.historique_model.update_lienIA(idElem, result)
        self._shared_variable["Chargement"] = False
        self.sharedVariableChanged.emit()


    def get_file_path(self, fileUrl: str) -> str:
        """
        Get the file path from the file URL.

        Args:
            fileUrl (str): The file URL.

        Returns:
            str: The file path.
        """
        if fileUrl.startswith("file:///"):
            if sys.platform == 'win32':
                return fileUrl[8:]
            elif sys.platform == 'darwin':
                raise Exception('macOS is not supported yet')
            else:
                return fileUrl[7:]
        return fileUrl
    
    def handle_media(self, file_path: str, is_url: bool = False):
        """
        Handle the media file.

        Args:
            file_path (str): The file path.
            is_url (bool, optional): Whether the file is a URL. Defaults to False.
        """
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
            self.infoSent.emit("wrong_file_type")
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
            
            if self.start == True :
                self.start = False
                self._shared_variable["Start"] = False
                self.sharedVariableChanged.emit()
            
        except Exception as e:
            self.infoSent.emit(f"Erreur : {e}")
    
    def handle_url(self, file_path: str):
        """
        Handle the URL.

        Args:
            file_path (str): The file path.
        """
        self.handle_media(file_path, is_url=True)
    
    def handle_file(self, file_path: str):
        """
        Handle the file.

        Args:
            file_path (str): The file path.
        """
        self.handle_media(file_path, is_url=False)

    @Slot()
    def start_Camera(self):
        """
        Start the camera recording.
        """
        self.pipelineCamera.start_camera_recording()

    @Slot()
    def stop_Camera(self):
        """
        Stop the camera recording.
        """
        self.pipelineCamera.stop_camera_recording()
    
    def on_recording_complete(self, lien: str):
        """
        Handle the completion of the recording.

        Args:
            lien (str): The file path of the recorded video.
        """
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
        """
        Open the file explorer to select a file.
        """
        try:
            destination_directory = get_base_data_dir() / "collections"
            os.makedirs(destination_directory, exist_ok=True)
            open_file_explorer(destination_directory)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de l'explorateur de fichiers : {e}")
            self.infoSent.emit(f"Erreur : {e}")

    @Slot()
    def openFileExplorer(self):
        """
        Open the file explorer to select images or videos.
        """
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
        """
        Toggle the visibility of the menu.
        """
        self._shared_variable["Menu"] = not self._shared_variable["Menu"]
        self.sharedVariableChanged.emit()
        
    @Slot()
    def toggle_erreur(self):
        """
        Toggle the visibility of the error message.
        """
        self._shared_variable["Erreur"] = not self._shared_variable["Erreur"]
        self.sharedVariableChanged.emit()

    @Slot()
    def toggle_camera(self):
        """
        Toggle the visibility of the camera.
        """
        self._shared_variable["Camera"] = not self._shared_variable["Camera"]
        self.sharedVariableChanged.emit()

    @Slot()
    def toggle_param(self):
        """
        Toggle the visibility of the settings menu.
        """
        self._shared_variable["settingsMenuShowed"] = not self._shared_variable["settingsMenuShowed"]
        self.sharedVariableChanged.emit()

    @Slot()
    def nouvelleDetection(self):
        """
        Start a new detection process.
        """
        pageID = self._internal_pageID
        self.media_model.clear_all_media()
        if self.start == False :
            self.start = True
            self._shared_variable["Start"] = True
            self.sharedVariableChanged.emit()
            
        self.fichier = {"id" : -1, "lien" : "", "type" : ""}
        self.increment_pageID()
    

    @Slot()
    def increment_pageID(self):
        """Incrémente le pageID pour une nouvelle détection et le met à jour pour les nouveaux éléments."""
        new_page_id = self.historique_model.get_max_pageID() + 1
        self._internal_pageID = new_page_id



    @Slot(int)
    def clearMediaData(self):
        """Efface les données actuelles de MediaData et récupère l'historique pour le pageID spécifié."""
        self.media_model.clear_all_media()


    
    @Slot()
    def goBackToPreviousPage(self, pageID):
        """Réinitialise les données de MediaData en fonction du pageID de la page précédente."""
        self.clearMediaData(pageID)
        
    
    
    @Slot(int)
    def deleteHistorique(self, pageIDToDelete):
        if pageIDToDelete == self._internal_pageID and self._shared_variable["Chargement"]:
            self.infoSent.emit(f"Ne pas effacer l'historique pendant le chargement d'une image")
            raise Exception("Ne pas effacer l'historique pendant le chargement d'une image")
            return

        self.historique_model.delete_by_pageID(pageIDToDelete)
        self.historique_model.remove_items_from_model(pageIDToDelete)

        if pageIDToDelete == self._internal_pageID:
            self.media_model.clear_all_media()

    def stop_detection(self):
        self._shared_variable["Chargement"] = False
        self._shared_variable["state"] = ""
        self.sharedVariableChanged.emit()

        if self.pipeline:
            self.pipeline.stop_processing()

        if self.pipelineCamera:
            self.pipelineCamera.stop_processing()

        print("Détection stoppée.")



    @Slot(int, str)
    def modifyPromptText(self, pageID, newText):
        old_title = self.historique_model.get_case_title(pageID)
        try:
            print("b")
            self.historique_model.update_case_title(pageID, newText)
            print("a")
            self.historique_model.update_items_by_pageID(pageID, newText)

        except (ValueError, LookupError) as e:
            self.infoSent.emit(str(e))


    @Property(str, notify=sharedVariableChanged)
    def getSizeOfHistory(self) -> str:
        """
        Get the size of the history.

        Returns:
            str: The size of the history.
        """
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
        """
        Delete the history.
        """
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
        
        pageID = set()
        for row in self.historique_model.historique_model._items:
            pageID.add(row["pageID"])
        
        for id in pageID:
            self.deleteHistorique(id)
        
        self.sharedVariableChanged.emit()
    
    def frame_send(self, frame: QImage):
        """
        Send the frame to the image provider.

        Args:
            frame (QImage): The frame to send.
        """
        self.image_provider.set_image(frame)

    @Slot(str, str, str, str)  
    def add_to_historique(self, prompt, lien, media_type, lienIA):
        if self._internal_pageID is None:
            print("Erreur : Aucun pageID courant défini.")
            return
        
        page_exists = self.historique_model.page_exists(self._internal_pageID)
        titre_case = prompt if not page_exists else ""

        new_id = self.historique_model.add_entry(
            pageID=self._internal_pageID,
            prompt=prompt,
            lien=lien,
            media_type=media_type,
            lienIA=lienIA,
            titre_case=titre_case            
        )

        new_item = {
            "id": new_id,
            "pageID": self._internal_pageID,
            "prompt": prompt,
            "lien": lienIA,
            "type": media_type,
            "lienIA": lien,
            "titre_case": titre_case
        }
        self.historique_model.add_item(new_item, self._internal_pageID)
        return new_id


    @Slot(int)
    def page_exists(self, pageID):
        """Vérifie si une case (Historique) existe pour un pageID donné."""
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM Historique WHERE pageID = ?", (pageID,))
            count = cursor.fetchone()[0]
            return count > 0

        except sqlite3.Error as e:
            print(f"Erreur lors de la vérification de l'existence de la page: {e}")
            return False
        finally:
            if connection:
                connection.close()

    
    @Slot(result=bool)
    def hasUnlocked100(self):
        return self._has_unlocked_100
    
    @Slot(float)
    def checkAndUnlock100(self, pourcentage):
        if pourcentage >= 100 and not self._has_unlocked_100:
            self._has_unlocked_100 = True
            self.celebrationUnlocked.emit()
    
    @Slot(int)
    def retrievePage(self, pageID):
        """Méthode appelée pour récupérer les données d'une page et les envoyer dans Media."""
        print(f"Début de récupération pour pageID = {pageID}")
        self.media_model.clear_all_media()
        rows = self.historique_model.get_entries_by_pageID(pageID)

        if not rows:
            self.infoSent.emit(f"Aucune donnée trouvée pour pageID {pageID}.")
            return

        self._internal_pageID = pageID
        for row in rows:
            id_row, prompt, file_path, media_type, lienIA = row
            media_id = self.media_model.addMediaItem(file_path, media_type)
            self.media_model.updateMediaItem(id=media_id, file_path=lienIA, file_path_ia=file_path, prompt=prompt)

        tmp = self.media_model.get_last_media()
        self.fichier = {"id": tmp["id"], "lien": tmp["lien"], "type": tmp["type"]}
        self._idChargement = tmp["id"]
        self._shared_variable["Chargement"] = False
        self.sharedVariableChanged.emit()

    @Slot()
    def startRecording(self):
        self.audio_recorder.start()

    @Slot()
    def stopRecording(self):
        self.audio_recorder.stop()
        res = self.audio_recorder.transcript()
        self.transcriptionReady.emit(res)