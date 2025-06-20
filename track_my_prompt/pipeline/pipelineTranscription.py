from PySide6.QtCore import QObject, Signal, Slot, QThread
import tempfile
import os
class WorkerTranscription(QObject):
    """
    Worker class to handle audio transcription in a separate thread.
    """
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, audio_bytes: bytes, parent: QObject = None):
        super().__init__(parent)
        self.audio_bytes = audio_bytes
        self._is_running = True

    def run_task(self):
        if not self._is_running:
            return
        try:
            import whisper
            model = whisper.load_model("base", device="cpu")
            with tempfile.NamedTemporaryFile(suffix=".wav", mode='wb', delete=False) as tmpfile:
                tmpfile.write(self.audio_bytes)
                tmpfile.flush()
                path_file = tmpfile.name
            result = model.transcribe(path_file)
            os.remove(path_file)
            self.finished.emit(result['text'])
        except Exception as e:
            print(e)
            self.error.emit(str(e))


    def stop(self):
        self._is_running = False

class PipelineTranscription(QObject):
    """
    PipelineTranscription class to manage audio transcription in a thread.
    """
    transcriptionComplete = Signal(str)
    transcriptionError = Signal(str)

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.thread = None
        self.worker = None

    @Slot(bytes)
    def start_transcription(self, audio_bytes: bytes):
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        self.thread = QThread()
        self.worker = WorkerTranscription(audio_bytes)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run_task)
        self.worker.finished.connect(self.on_transcription_complete)
        self.worker.error.connect(self.on_transcription_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    @Slot(str)
    def on_transcription_complete(self, text: str):
        self.transcriptionComplete.emit(text)

    @Slot(str)
    def on_transcription_error(self, error: str):
        self.transcriptionError.emit(error)