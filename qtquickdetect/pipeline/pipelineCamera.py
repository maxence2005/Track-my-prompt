import cv2
import uuid
import os
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtGui import QImage
from utils.filepaths import get_base_data_dir

class CameraWorker(QObject):
    resultReady = Signal(str)      # Signal pour transmettre le chemin du fichier
    errorOccurred = Signal(str)
    frameCaptured = Signal(QImage) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = True     # État d'enregistrement
        self.file_path = None       # Chemin du fichier à sauvegarder

    def run_task(self):
        # Ouvre la caméra
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            capture =cv2.VideoCapture(1)
            if not capture.isOpened():
                self.errorOccurred.emit("Erreur : Impossible d'ouvrir la caméra.")
                return

        # Prépare le dossier et le nom du fichier
        destination_directory = get_base_data_dir() / "collections" / "video"
        os.makedirs(destination_directory, exist_ok=True)
        self.file_path = destination_directory / f"webcam_capture_{str(uuid.uuid4())}.avi"

        # Configuration de l'enregistrement vidéo
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(str(self.file_path), fourcc, fps, (frame_width, frame_height))

        # Boucle de capture d'images
        while self._is_running:
            ret, frame = capture.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Émettre le signal avec l'image capturée
            self.frameCaptured.emit(q_image)

            out.write(frame)

        # Libération des ressources
        capture.release()
        out.release()

        # Émettre le signal avec le chemin du fichier, qu'il y ait interruption ou fin normale
        self.resultReady.emit(str(self.file_path))

    def stop(self):
        """Interrompt la capture en fixant _is_running à False."""
        self._is_running = False


class CameraPipeline(QObject):
    processingComplete = Signal(str)   # Signal pour transmettre le fichier terminé
    on_error = Signal(str)  
    frame_send = Signal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None

    @Slot()
    def start_camera_recording(self):
        """Démarre l'enregistrement de la caméra dans un thread séparé."""
        self.thread = QThread()
        self.worker = CameraWorker()
        
        # Connecter les signaux du worker
        self.worker.resultReady.connect(self.on_processing_complete)
        self.worker.frameCaptured.connect(self.captured_image)
        self.worker.errorOccurred.connect(self.on_error_occurred)
        
        # Déplacer le worker dans le thread et démarrer le thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_task)

        # Nettoyage après fin du traitement
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        # Démarrer le thread
        self.thread.start()

    @Slot()
    def stop_camera_recording(self):
        """Arrête l'enregistrement de la caméra et émet le fichier généré."""
        self.stop_processing()

    @Slot(str)
    def on_processing_complete(self, file_path):
        """Recevoir le chemin du fichier généré à la fin de l'enregistrement."""
        self.processingComplete.emit(file_path)
        self.stop_processing()
    
    @Slot(QImage)
    def captured_image(self, frame):
        self.frame_send.emit(frame)

    @Slot(str)
    def on_error_occurred(self, error_message):
        self.on_error.emit(error_message)
        self.stop_processing()

    def stop_processing(self):
        """Arrête le thread d'enregistrement et libère les ressources."""
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()
