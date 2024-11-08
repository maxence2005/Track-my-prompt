import os
import uuid
import shutil
import re
from pathlib import Path
from ultralytics import YOLOWorld
from utils import filepaths
from PySide6.QtCore import QObject, Signal, Slot, QThread

def traitementPrompt(filePath: str, classes: list = None, typ: str = None) -> str:
    models_path = filepaths.get_base_data_dir() / 'models'
    model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))
    
    if classes:
        model.set_classes(classes)
    
    collections_dir = filepaths.get_base_data_dir() / 'collections'
    if typ == "image":
        collections_dir = collections_dir / "image"
    else:
        collections_dir = collections_dir / "video"

    os.makedirs(collections_dir, exist_ok=True)

    results = model.predict(filePath, save=True, save_dir=str(collections_dir), exist_ok=True)
    saved_image_path = results[0].save_dir
    filePath_without_extension = os.path.splitext(filePath)[0]
    saved_files = list(Path(saved_image_path).glob(os.path.basename(filePath_without_extension)+'*'))[0]

    final_image_path = collections_dir / f"ia_{str(uuid.uuid4())}"
    shutil.move(saved_image_path, final_image_path)

    f = final_image_path / os.path.basename(saved_files)
    return str(f)


class Worker(QObject):
    resultReady = Signal(str)

    def __init__(self, filePath, classes=None, typ="image", parent=None):
        super().__init__(parent)
        self.filePath = filePath
        self.classes = classes
        self.typ = typ
        self._is_running = True

    def run_task(self):
        """Exécute la fonction traitementPrompt sur un thread séparé."""
        if self._is_running:
            result = traitementPrompt(self.filePath, self.classes, self.typ)
            self.resultReady.emit(result) 

    def stop(self):
        """Permet d'arrêter le traitement si nécessaire."""
        self._is_running = False


class PipelinePrompt(QObject):
    processingComplete = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.promptText = None

    @Slot(str, list, str, str)
    def start_processing(self, filePath, classes=None, typ="image", promptText=""):
        """Initialise et démarre le thread pour traitementPrompt."""
        # Créer un thread et un worker pour exécuter la tâche
        self.thread = QThread()
        self.worker = Worker(filePath, classes, typ)
        self.promptText = promptText
        # Connecter le signal du worker au signal du pipeline
        self.worker.resultReady.connect(self.on_processing_complete)

        # Déplacer le worker dans le thread séparé et démarrer le thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_task)

        # Nettoyer après la fin du traitement
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        # Démarrer le thread
        self.thread.start()

    @Slot(str)
    def on_processing_complete(self, result):
        """Réceptionne les résultats et émet un signal vers le thread principal."""
        self.processingComplete.emit(result, self.promptText)
        self.stop_processing()

    def stop_processing(self):
        """Arrêter le thread."""
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()


def promptFiltre(phrase: str) -> list:

    available_classes = ["person", "backpack", "umbrella", "handbag", "suitcase", "tie", "bicycle", "car",
        "motorcycle", "airplane", "train", "bus", "truck", "boat", "traffic light",
        "fire hydrant", "stop sign", "parking meter", "bench", "sheep", "cow", "cat",
        "horse", "dog", "bird", "elephant", "bear", "baseball glove", "kite", "giraffe",
        "zebra", "tennis racket", "skateboard", "sports ball", "baseball bat",
        "snowboard", "frisbee", "skis", "bottle", "wine glass", "fork", "cup", "knife",
        "spoon", "bowl", "cake", "donut", "hot dog", "pizza", "carrot", "broccoli",
        "sandwich", "orange", "apple", "banana", "couch", "chair", "potted plant",
        "bed", "toilet", "dining table", "keyboard", "cell phone", "remote", "laptop",
        "tv", "mouse", "microwave", "oven", "sink", "toaster", "refrigerator",
        "teddy bear", "hair drier", "toothbrush", "scissors", "clock", "book", "vase"]

    phrase = phrase.lower()
    phrase = re.sub(r'[^\w\s]', '', phrase)
    

    words = phrase.split()
    

    filtered_classes = [word for word in words if word in available_classes]
    
    return filtered_classes
