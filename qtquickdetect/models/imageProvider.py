from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage
from PySide6.QtCore import QSize

class ImageProvider(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)
        self._image = QImage(640, 480, QImage.Format_RGB888)

    def set_image(self, image: QImage):
        self._image = image

    def requestImage(self, id, size, requestedSize):
        return self._image