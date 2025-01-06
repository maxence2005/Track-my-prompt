import os
from models.traitement_ia import traitementPrompt
from models.filtre import promptFiltre
from PySide6.QtCore import QObject, Signal, Slot, QThread
from models.encylo import EncyclopediaModel

class Worker(QObject):
    def __init__(self, pipelinePrompt, filePath, promptText="", typ="image", parent=None, method="dumb", api_key="", encyclo_model: EncyclopediaModel = None):
        super().__init__(parent)
        self.filePath = filePath
        self.prompt = promptText
        self.typ = typ
        self._is_running = True
        self.method = method
        self.api_key = api_key
        self.pipeline = pipelinePrompt
        self.encyclo_model = encyclo_model

    def run_task(self):
        if self._is_running:
            try:
                classes = promptFiltre(self.prompt, self.method, self.api_key)
            except Exception as e:
                self.pipeline.on_error_occurred("prompt")
                return
            result = traitementPrompt(self.filePath, classes, self.typ, self.encyclo_model)
            self.pipeline.on_processing_complete(result)
            
    def stop(self):
        self._is_running = False

class PipelinePrompt(QObject):
    def __init__(self, backend, parent=None, encyclo_model: EncyclopediaModel = None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.promptText = None
        self.backend = backend
        self.encyclo_model = encyclo_model

    @Slot(str, str, str, str, str)
    def start_processing(self, filePath, typ="image", promptText="", method="dumb", api_key=""):
        self.thread = QThread()
        self.worker = Worker(self, filePath, promptText, typ, method=method, api_key=api_key, encyclo_model=self.encyclo_model)
        self.promptText = promptText

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run_task)

        # Nettoyage
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        self.thread.start()

    @Slot(object)
    def on_processing_complete(self, result):
        self.backend.on_processing_complete(result, self.promptText)
        self.stop_processing()

    @Slot(str)
    def on_error_occurred(self, error):
        self.backend.on_processing_complete(None, None)
        if error == "prompt":
            self.backend.infoSent.emit("prompt_err")
        self.stop_processing()

    def stop_processing(self):
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()