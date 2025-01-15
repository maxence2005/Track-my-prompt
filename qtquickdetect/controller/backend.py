import sys
import os
import shutil
import sqlite3
from urllib.parse import urlparse
from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal, QUrl, Property
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QImage

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

    def __init__(self, media_model: DatabaseManagerMedia, row: int, db_path: str, historique_model: QObject, im_pro: ImageProvider, prompt_ia: str, api_key_mistral: str, encyclopedia_model: QObject):
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
        self._shared_variable = {"settingsMenuShowed": False, "Erreur": False, "Menu": True, "Chargement" : False, "prompt_ia" : prompt_ia, "api_key_mistral" : api_key_mistral, "Camera" : False, "state" : ""}
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
        if self.start == True :
            self.start = False
            self._shared_variable["Start"] = False
            self.sharedVariableChanged.emit()
            
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
        
        if result is not None:
            self.media_model.updateMediaItem(id=self.fichier["id"], file_path_ia=result, prompt=promptText)
            
            # Mise à jour de la table Historique pour le fichier traité
            connection = None
            try:
                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()
                # Met à jour le champ lienIA avec le résultat retourné
                cursor.execute("""
                    UPDATE Historique
                    SET lien = ?
                    WHERE id = ?
                """, (result, idElem))
                
                connection.commit()
                print(f"[DEBUG] Mise à jour de la base de données pour l'ID {self.fichier['id']} avec lienIA : {result}")
                
                # Afficher tout l'historique pour débogage
                cursor.execute("SELECT * FROM Historique")
                all_rows = cursor.fetchall()
                print("[DEBUG] Contenu complet de la table Historique :")
                for row in all_rows:
                    print(row)

            except sqlite3.Error as e:
                print(f"[ERROR] Erreur lors de la mise à jour de la base de données : {e}")
                self.infoSent.emit(f"Erreur de mise à jour dans la base de données : {e}")
            finally:
                if connection:
                    connection.close()
                    print("Connexion à la base de données fermée après mise à jour.")

        # Mise à jour des variables partagées et émission du signal
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
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Incrémenter le pageID actuel pour la nouvelle détection
            cursor.execute("SELECT MAX(pageID) FROM Historique")
            max_page_id = cursor.fetchone()[0]
            new_page_id = (max_page_id or 0) + 1
            self._internal_pageID = new_page_id  # Mise à jour de la variable _internal_pageID

            print(f"Nouvelle pageID générée : {self._internal_pageID}")

        except sqlite3.Error as e:
            print(f"Erreur lors de l'incrémentation du pageID: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(int)
    def clearMediaData(self):
        """Efface les données actuelles de MediaData et récupère l'historique pour le pageID spécifié."""
        # Vider MediaData
        self.media_model.clear_all_media()


    
    @Slot()
    def goBackToPreviousPage(self, pageID):
        """Réinitialise les données de MediaData en fonction du pageID de la page précédente."""
        self.clearMediaData(pageID)
        
    @Slot(int)
    def deleteHistorique(self, pageIDToDelete):
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Supprimer tous les éléments ayant le même pageID
            cursor.execute("DELETE FROM Historique WHERE pageID = ?", (pageIDToDelete,))
            connection.commit()

            # Supprimer les éléments dans le modèle correspondant à ce pageID
            self.historique_model.remove_items_from_model(pageIDToDelete)

            if pageIDToDelete == self._internal_pageID:
                self.media_model.clear_all_media()


            print(f"Tous les éléments avec pageID {pageIDToDelete} ont été supprimés.")
        except sqlite3.Error as e:
            self.infoSent.emit(f"Erreur lors de la suppression de l'élément: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(int, str)
    def modifyPromptText(self, pageID, newText):
        """Modifie le texte du prompt pour tous les éléments ayant la même pageID dans la base de données et met à jour le modèle."""
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Mettre à jour tous les éléments avec la pageID donnée
            cursor.execute("UPDATE Historique SET prompt = ? WHERE pageID = ?", (newText, pageID))
            connection.commit()

            # Si des lignes ont été mises à jour, mettez à jour le modèle
            if cursor.rowcount > 0:
                self.historique_model.update_items_by_pageID(pageID, newText)

        except sqlite3.Error as e:
            self.infoSent.emit(f"Erreur lors de la modification du texte du prompt: {e}")
        finally:
            if connection:
                connection.close()


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
        self.sharedVariableChanged.emit()
    
    def frame_send(self, frame: QImage):
        """
        Send the frame to the image provider.

        Args:
            frame (QImage): The frame to send.
        """
        self.image_provider.set_image(frame)

    @Slot(str, str, str, str)  # Ex : prompt, lien, type, lienIA
    def add_to_historique(self, prompt, lien, media_type, lienIA):
        """Ajoute un élément à l'historique pour la page actuelle."""
        if self._internal_pageID is None:
            print("Erreur : Aucun pageID courant défini. Impossible d'ajouter un élément.")
            return

        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Insertion dans la base de données avec le _internal_pageID
            cursor.execute(
                """
                INSERT INTO Historique (pageID, prompt, lien, type, lienIA)
                VALUES (?, ?, ?, ?, ?)
                """,
                (self._internal_pageID, prompt, lienIA, media_type, lien),
            )
            connection.commit()

            # Récupération de l'ID auto-généré
            new_id = cursor.lastrowid

            # Mise à jour du modèle uniquement si c'est pour la page actuelle
            new_item = {
                "id": new_id,
                "pageID": self._internal_pageID,
                "prompt": prompt,
                "lien": lienIA,
                "type": media_type,
                "lienIA": lien,
            }
            self.historique_model.add_item(new_item,self._internal_pageID)

            print(f"Nouvel élément ajouté pour pageID {self._internal_pageID}: {new_item}")
            print(f"voici l'id dans add_to_historique : {new_id}")
            return new_id

        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
        finally:
            if connection:
                connection.close()

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

    @Slot(int)
    def retrievePage(self, pageID):
        """Méthode appelée pour récupérer les données d'une page et les envoyer dans Media."""
        print(f"Début de récupération pour pageID = {pageID}")
        self.media_model.clear_all_media()  # Nettoyer les médias actuels

        connection = None
        try:
            # Connexion à la base de données
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            
            # Requête SQL pour récupérer les données
            cursor.execute("""
                SELECT id,prompt, lien, type, lienIA
                FROM Historique
                WHERE pageID = ?
            """, (pageID,))
            rows = cursor.fetchall()
            self._internal_pageID = pageID
            if not rows:
                self.infoSent.emit(f"Aucune donnée trouvée pour pageID {pageID}.")
                print(f"Aucune donnée trouvée pour pageID {pageID}")
                return

            for row in rows:
                id_row, prompt, file_path, media_type, lienIA = row
                print(f"Ajout d'un élément : {row}")
                id_row = self.media_model.addMediaItem(file_path, media_type)
                print(f"voici le id_row apres modifs : {id_row}")
                self.media_model.updateMediaItem(id=id_row,file_path=lienIA, file_path_ia=file_path, prompt=prompt)

            tmp = self.media_model.get_last_media()
            self.fichier = {"id": tmp["id"], "lien" : tmp["lien"], "type" : tmp["type"]}
            self._idChargement = tmp["id"]
            self._shared_variable["Chargement"] = False
            self.sharedVariableChanged.emit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération : {e}")
            self.infoSent.emit(f"Erreur lors de la récupération : {e}")
        finally:
            if connection:
                connection.close()
                print("Connexion à la base de données fermée.") 