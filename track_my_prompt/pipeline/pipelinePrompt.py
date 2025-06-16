import os
from models.traitement_ia import traitementPrompt
from models.filtre import promptFiltre
from PySide6.QtCore import QObject, Signal, Slot, QThread
from models.encylo import EncyclopediaModel
from utils.color_utils import hex_to_bgr

class Worker(QObject):
    """
    Worker class to handle the processing of prompts in a separate thread.
    """
    def __init__(self, pipelinePrompt: 'PipelinePrompt', filePath: str, promptText: str = "", typ: str = "image", parent: QObject = None, method: str = "dumb", api_key: str = "", encyclo_model: EncyclopediaModel = None, backend: QObject = None):
        """
        Initialize the Worker with the given parameters.

        Args:
            pipelinePrompt (PipelinePrompt): The pipeline prompt instance.
            filePath (str): The file path to process.
            promptText (str, optional): The prompt text. Defaults to "".
            typ (str, optional): The type of the file. Defaults to "image".
            parent (QObject, optional): The parent object. Defaults to None.
            method (str, optional): The method to use for filtering. Defaults to "dumb".
            api_key (str, optional): The API key for the method. Defaults to "".
            encyclo_model (EncyclopediaModel, optional): The encyclopedia model. Defaults to None.
            backend (QObject, optional): The backend object. Defaults to None.
        """
        super().__init__(parent)
        self.filePath = filePath
        self.prompt = promptText
        self.typ = typ
        self._is_running = True
        self.method = method
        self.api_key = api_key
        self.pipeline = pipelinePrompt
        self.encyclo_model = encyclo_model
        self.backend = backend

        hex_color = self.pipeline.backend.shared_variable.get("frame_color", "#00FF00")
        self.color = hex_to_bgr(hex_color)

    def run_task(self):
        """
        Run the task to process the prompt.
        """
        if self._is_running:
            try:
                print(f"[DEBUG] Appel à promptFiltre avec prompt={self.prompt}, method={self.method}, api_key={self.api_key}")
                classes = promptFiltre(self.prompt, self.method, self.api_key)
            except Exception as e:
                self.pipeline.on_error_occurred("prompt")
                return
            if self.backend is not None:
                self.backend._shared_variable["state"] = "ia"
                self.backend.sharedVariableChanged.emit()
            else:
                print("Erreur: backend non défini")
            result = traitementPrompt(self.filePath, classes, self.typ, self.encyclo_model, self.color)
            self.pipeline.on_processing_complete(result)
            
    def stop(self):
        """
        Stop the worker.
        """
        self._is_running = False

class PipelinePrompt(QObject):
    """
    PipelinePrompt class to manage the processing of prompts.
    """
    def __init__(self, backend: QObject, parent: QObject = None, encyclo_model: EncyclopediaModel = None):
        """
        Initialize the PipelinePrompt with the given parameters.

        Args:
            backend (QObject): The backend object.
            parent (QObject, optional): The parent object. Defaults to None.
            encyclo_model (EncyclopediaModel, optional): The encyclopedia model. Defaults to None.
        """
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.promptText = None
        self.current_id = -1
        self.backend = backend
        self.encyclo_model = encyclo_model

    @Slot(str, str, str, str, str,str)
    def start_processing(self, filePath: str, typ: str = "image", promptText: str = "", method: str = "dumb", api_key: str = "",id = -1):
        """
        Start processing the prompt in a separate thread.

        Args:
            filePath (str): The file path to process.
            typ (str, optional): The type of the file. Defaults to "image".
            promptText (str, optional): The prompt text. Defaults to "".
            method (str, optional): The method to use for filtering. Defaults to "dumb".
            api_key (str, optional): The API key for the method. Defaults to "".
        """
        print(f"[DEBUG] Démarrage du traitement avec filePath={filePath}, typ={typ}, promptText={promptText}, method={method}, api_key={api_key}")
        self.thread = QThread()
        self.worker = Worker(self, filePath, promptText, typ, method=method, api_key=api_key, encyclo_model=self.encyclo_model, backend=self.backend)
        self.promptText = promptText
        self.current_id = id
        print(f"voici l'id dans start_processing : {self.current_id}")

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run_task)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        self.thread.start()

    @Slot(object)
    def on_processing_complete(self, result: object):
        """
        Handle the completion of the processing.

        Args:
            result (object): The result of the processing.
        """
        self.backend.on_processing_complete(result, self.promptText, self.current_id)
        self.stop_processing()

    @Slot(str)
    def on_error_occurred(self, error: str):
        """
        Handle errors that occur during processing.

        Args:
            error (str): The error message.
        """
        self.backend.on_processing_complete(None, self.promptText, self.current_id)
        if error == "prompt":
            self.backend.infoSent.emit("prompt_err")
        self.stop_processing()

    def stop_processing(self):
        """
        Stop the processing.
        """
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()