
import os
from models.traitement_ia import traitementPrompt
from models.filtre import promptFiltre
from PySide6.QtCore import QObject, Signal, Slot, QThread

class Worker(QObject):
    resultReady = Signal(str)

    def __init__(self, filePath, promptText="", typ="image", parent=None, method="dumb", api_key=""):
        super().__init__(parent)
        self.filePath = filePath
        self.prompt = promptText
        self.typ = typ
        self._is_running = True
        self.method = method
        self.api_key = api_key

    def run_task(self):
        if self._is_running:
            try:
                classes = promptFiltre(self.prompt, self.method, self.api_key)
            except ValueError as e:
                pass # TODO: handle error
            result = traitementPrompt(self.filePath, classes, self.typ)
            self.resultReady.emit(result)

    def stop(self):
        self._is_running = False


class PipelinePrompt(QObject):
    processingComplete = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.promptText = None

    @Slot(str, list, str, str)
    def start_processing(self, filePath, typ="image", promptText="", method="dumb", api_key=""):
        self.thread = QThread()
        self.worker = Worker(filePath, promptText, typ, method=method, api_key=api_key)
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
