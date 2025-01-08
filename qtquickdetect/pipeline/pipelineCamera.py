import cv2
import uuid
import os
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtGui import QImage
from utils.filepaths import get_base_data_dir

class CameraWorker(QObject):
    frameCaptured = Signal(QImage)

    def __init__(self, pipeline, parent=None):
        super().__init__(parent)
        self._is_running = True    
        self.file_path = None     
        self.pipeline = pipeline
        
    def run_task(self):
        """
        Runs the video record
        """
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            capture =cv2.VideoCapture(1)
            if not capture.isOpened():
                self.pipeline.on_error_occurred("Erreur : Impossible d'ouvrir la caméra.")
                return

        destination_directory = get_base_data_dir() / "collections" / "video"
        os.makedirs(destination_directory, exist_ok=True)
        self.file_path = destination_directory / f"webcam_capture_{str(uuid.uuid4())}.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(str(self.file_path), fourcc, fps, (frame_width, frame_height))

        while self._is_running:
            ret, frame = capture.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            self.pipeline.captured_image(q_image)
            out.write(frame)

        capture.release()
        out.release()

        self.pipeline.on_processing_complete(str(self.file_path))

    def stop(self):
        self._is_running = False


class CameraPipeline(QObject):
    on_error = Signal(str)
    frame_send = Signal(QImage)

    def __init__(self, backend, parent=None):
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.backend = backend

    @Slot()
    def start_camera_recording(self):
        """
        Starts the record
        """
        self.thread = QThread()
        self.worker = CameraWorker(self)
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_task)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker.deleteLater)

        self.thread.start()

    @Slot()
    def stop_camera_recording(self):
        """
        Stops the record
        """
        self.stop_processing()

    @Slot(str)
    def on_processing_complete(self, file_path):
        self.backend.on_recording_complete(file_path)
        self.stop_processing()
    
    @Slot(QImage)
    def captured_image(self, frame):
        self.frame_send.emit(frame)

    @Slot(str)
    def on_error_occurred(self, error_message):
        self.on_error.emit(error_message)
        self.stop_processing()

    def stop_processing(self):
        """
        Stops the process
        """
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
