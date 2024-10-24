import sys
import os
import shutil
from PySide6.QtCore import QObject, Slot, Signal, QUrl, Property
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtQml import QQmlApplicationEngine


class Backend(QObject):
    # Déclarez un signal
    infoSent = Signal(str)
    sharedVariableChanged = Signal()

    def __init__(self):
        super().__init__()
        self._shared_variable = {"settingsMenuShowed": False}

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
        print(f"Received prompt: {promptText}")
        # Traitez le texte ici
        # Émettez le signal avec les informations
        self.infoSent.emit(f"Processed: {promptText}")

    @Slot(str)
    def receiveFile(self, fileUrl):
        # Extraire le chemin du fichier
        if fileUrl.startswith("file:///"):
            file_path = fileUrl[8:]  # Enlève le préfixe "file:///"
        else:
            file_path = fileUrl

        # Définir le répertoire de destination
        destination_directory = os.path.join(
            os.path.dirname(__file__), "../resources/save")

        # Assurez-vous que le répertoire de destination existe
        os.makedirs(destination_directory, exist_ok=True)

        try:
            # Copier le fichier dans le répertoire de destination
            shutil.copy(file_path, destination_directory)
            print(f"Fichier {file_path} enregistré avec succès dans {
                  destination_directory}")
            self.infoSent.emit(f"Fichier enregistré : {file_path}")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du fichier : {e}")
            self.infoSent.emit(f"Erreur : {e}")

    @Slot()
    def openFileExplorer(self):
        # Ouvrir la boîte de dialogue pour sélectionner un fichier
        file_dialog = QFileDialog()
        # Pour permettre la sélection de fichiers existants
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("All Files (*)")  # Filtrer tous les fichiers
        file_dialog.setViewMode(QFileDialog.List)  # Mode d'affichage en liste

        if file_dialog.exec():
            # Récupérer les fichiers sélectionnés
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # Appeler la méthode pour traiter le fichier sélectionné
                self.receiveFile(selected_files[0])
