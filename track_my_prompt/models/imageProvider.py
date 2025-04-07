from PySide6.QtQuick import QQuickImageProvider
from PySide6.QtGui import QImage
from PySide6.QtCore import QSize

class ImageProvider(QQuickImageProvider):
    def __init__(self):
        """
        Initialize the ImageProvider.
        """
        super().__init__(QQuickImageProvider.Image)
        self._image = QImage(640, 480, QImage.Format_RGB888)

    def set_image(self, image: QImage):
        """
        Set the image to be provided.

        Args:
            image (QImage): The image to set.
        """
        self._image = image

    def requestImage(self, id: str, size: QSize, requestedSize: QSize) -> QImage:
        """
        Request the image.

        Args:
            id (str): The ID of the image.
            size (QSize): The size of the image.
            requestedSize (QSize): The requested size of the image.

        Returns:
            QImage: The requested image.
        """
        return self._image