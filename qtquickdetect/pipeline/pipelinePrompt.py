
import os
from models.traitement_ia import traitementPrompt
from models.filtre import promptFiltre
from PySide6.QtCore import QObject, Signal, Slot, QThread

class Worker(QObject):
    resultReady = Signal(str)

    def __init__(self, pipelinePrompt, filePath, promptText="", typ="image", parent=None):
        super().__init__(parent)
        self.filePath = filePath
        self.prompt = promptText
        self.typ = typ
        self._is_running = True
        self.pipelinePrompt = pipelinePrompt

    def run_task(self):
        if self._is_running:
            classes = promptFiltre(self.prompt)
            result = traitementPrompt(self.filePath, classes, self.typ)
            self.pipelinePrompt.on_processing_complete(result)

    def stop(self):
        self._is_running = False


class PipelinePrompt(QObject):
    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.promptText = None
        self.backend = backend

    @Slot(str, list, str)
    def start_processing(self, filePath, typ="image", promptText=""):
        self.thread = QThread()
        self.worker = Worker(self, filePath, promptText, typ)
        self.promptText = promptText

        # Déplacer le worker dans le thread séparé et démarrer le thread
        self.worker.moveToThread(self.thread)
        
        # Connecter le signal du worker au signal du pipeline
        self.thread.started.connect(self.worker.run_task)

        # Nettoyer après la fin du traitement
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        # Démarrer le thread
        self.thread.start()

    @Slot(str)
    def on_processing_complete(self, result):
        """Réceptionne les résultats et émet un signal vers le thread principal."""
        self.backend.on_processing_complete(result, self.promptText)
        self.stop_processing()

    def stop_processing(self):
        """Arrêter le thread."""
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()
