import sqlite3
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

class MediaModel(QAbstractListModel):
    """
    MediaModel is a QAbstractListModel that holds media items with roles for link, type, and prompt.
    """
    # Define the roles for the model elements
    LinkRole = Qt.UserRole + 1
    TypeRole = Qt.UserRole + 2
    PromptRole = Qt.UserRole + 3

    def __init__(self, *args, **kwargs):
        """
        Initialize the MediaModel.

        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        """
        super(MediaModel, self).__init__(*args, **kwargs)
        self._items = []

    def data(self, index, role):
        """
        Retrieve data for the given index and role.

        :param index: QModelIndex
        :param role: int
        :return: Data corresponding to the role
        """
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None
        
        item = self._items[index.row()]

        if role == self.LinkRole:
            return item["lien"]
        elif role == self.TypeRole:
            return item["type"]
        elif role == self.PromptRole:
            return item["prompt"]
        return None

    def rowCount(self, parent=QModelIndex()):
        """
        Return the number of rows in the model.

        :param parent: QModelIndex
        :return: int
        """
        return len(self._items)

    def roleNames(self):
        """
        Map roles to property names for use in QML.

        :return: dict
        """
        return {
            self.LinkRole: b"lien",
            self.TypeRole: b"type",
            self.PromptRole: b"prompt",
        }

    def update_data(self, data):
        """
        Replace the current model data with new data.

        :param data: list of dict
        :return: None
        """
        self.beginResetModel()
        self._items = data
        self.endResetModel()

    @Slot(str, str, str)
    def addMediaItem(self, file_path, media_type, prompt=""):
        """
        Add a new media item to the model.

        :param file_path: str
        :param media_type: str
        :param prompt: str
        :return: None
        """
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append({"lien": file_path, "type": media_type, "prompt": prompt})
        self.endInsertRows()
    

class DatabaseManagerMedia(QObject):
    """
    DatabaseManagerMedia handles database operations and manages the MediaModel.
    """
    dataLoaded = Signal()

    def __init__(self, db_path, parent=None):
        """
        Initialize the DatabaseManagerMedia.

        :param db_path: str
        :param parent: QObject
        """
        super().__init__(parent)
        self.db_path = db_path
        self._media_model = MediaModel()
        self.load_data()

    @Slot()
    def load_data(self):
        """
        Load data from the database and update the media model.

        :return: None
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT lien, type, prompt FROM MediaData")
            rows = cursor.fetchall()

            # Convert data to dictionaries for the model
            data = [{"lien": row[0], "type": row[1], "prompt": row[2] if row[2] else ""} for row in rows]
            self._media_model.update_data(data)  # Update the media model

            self.dataLoaded.emit()  # Emit the signal to indicate data has been loaded

        except sqlite3.Error as e:
            print(f"Error accessing the database: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(str, str, str)
    def addMediaItem(self, file_path, media_type, prompt=""):
        """
        Add a new media item to the model and insert it into the database.

        :param file_path: str
        :param media_type: str
        :param prompt: str
        :return: None
        """
        self._media_model.addMediaItem(file_path, media_type, prompt)
        self.insert_into_database(file_path, media_type, prompt)

    def insert_into_database(self, file_path, media_type, prompt):
        """
        Insert a new media item into the database.

        :param file_path: str
        :param media_type: str
        :param prompt: str
        :return: None
        """
        file_path = str(file_path)
        media_type = str(media_type)
        prompt = str(prompt)
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Use a prepared statement to avoid SQL injection
            cursor.execute("INSERT INTO MediaData (lien, type, prompt) VALUES (?, ?, ?)", 
                           (file_path, media_type, prompt))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting into the database: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(result=dict)
    def get_last_media(self):
        """
        Retrieve the last recorded media item from the database.

        :return: dict
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT lien, type, prompt FROM MediaData ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return {"lien": row[0], "type": row[1], "prompt": row[2]}
            else:
                return {}  # Return an empty dictionary if no media found
        except sqlite3.Error as e:
            print(f"Error retrieving the last media: {e}")
            return {}
        finally:
            if connection:
                connection.close()

    @Slot()
    def clear_all_media(self):
        """
        Delete all records from the MediaData table and update the model.

        :return: None
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM MediaData")
            connection.commit()
            # Update the model to reflect the deletion
            self._media_model.update_data([])
        except sqlite3.Error as e:
            print(f"Error deleting media: {e}")
        finally:
            if connection:
                connection.close()

    @Property(QObject, constant=True)
    def mediaModel(self):
        """
        Expose mediaModel to QML.

        :return: MediaModel
        """
        return self._media_model
