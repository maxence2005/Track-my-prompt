import cv2
import uuid
from PySide6.QtCore import QObject, Signal, Slot, QThread
from PySide6.QtGui import QImage
from utils.filepaths import get_base_data_dir
from ultralytics import YOLOWorld
import torch
import os
from utils import filepaths
import random

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class CameraWorker(QObject):
    frameCaptured = Signal(QImage)

    def __init__(self, pipeline: 'CameraPipeline', parent: QObject = None):
        """
        Initialize the CameraWorker with the given parameters.

        Args:
            pipeline (CameraPipeline): The camera pipeline instance.
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self._is_running = True
        self.file_path = None
        self.pipeline = pipeline
        models_path = filepaths.get_base_data_dir() / 'models'
        self.model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt')).to(device)

        
    def run_task(self):
        """
        Runs the video recording task.
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

        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        while self._is_running:
            ret, frame = capture.read()
            if not ret:
                break
            
            with torch.no_grad():
                results = self.model.predict(frame, stream=True)

                for r in results:
                    for i, box in enumerate(r.boxes.xyxy):
                        x1, y1, x2, y2 = map(int, box)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                        if r.boxes.conf is not None and i < len(r.boxes.conf):
                            confidence = r.boxes.conf[i].item() * 100
                            class_index = int(r.boxes.cls[i].item())
                            class_name = self.model.names[class_index] if class_index in self.model.names else "Unknown"
                            label = f"{class_name} {confidence:.1f}%"
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

                    if r.masks is not None:
                        r.masks.draw(frame)
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
        """
        Stop the worker.
        """
        self._is_running = False


class CameraPipeline(QObject):
    on_error = Signal(str)
    frame_send = Signal(QImage)

    def __init__(self, backend: QObject, parent: QObject = None):
        """
        Initialize the CameraPipeline with the given parameters.

        Args:
            backend (QObject): The backend object.
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self.thread = None
        self.worker = None
        self.backend = backend

    @Slot()
    def start_camera_recording(self):
        """
        Start the camera recording in a separate thread.
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
        Stop the camera recording.
        """
        self.stop_processing()

    @Slot(str)
    def on_processing_complete(self, file_path: str):
        """
        Handle the completion of the recording.

        Args:
            file_path (str): The path to the recorded file.
        """
        self.backend.on_recording_complete(file_path)
        self.stop_processing()
    
    @Slot(QImage)
    def captured_image(self, frame: QImage):
        """
        Emit the captured image signal.

        Args:
            frame (QImage): The captured image.
        """
        self.frame_send.emit(frame)

    @Slot(str)
    def on_error_occurred(self, error_message: str):
        """
        Handle errors that occur during recording.

        Args:
            error_message (str): The error message.
        """
        self.on_error.emit(error_message)
        self.stop_processing()

    def stop_processing(self):
        """
        Stop the processing.
        """
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
