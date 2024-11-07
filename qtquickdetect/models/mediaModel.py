import sqlite3
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt


class MediaModel(QAbstractListModel):
    """
    MediaModel is a QAbstractListModel that holds media items with roles for id, link, type, prompt, and lienIA.
    """
    # Define the roles for the model elements
    IdRole = Qt.UserRole + 1
    LinkRole = Qt.UserRole + 2
    TypeRole = Qt.UserRole + 3
    PromptRole = Qt.UserRole + 4
    LienIARole = Qt.UserRole + 5

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
        item["index"] = index.row()
        if role == self.IdRole:
            return str(item["id"])
        elif role == self.LinkRole:
            return item["lien"]
        elif role == self.TypeRole:
            return item["type"]
        elif role == self.PromptRole:
            return item["prompt"]
        elif role == self.LienIARole:
            return item["lienIA"]
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
            self.IdRole: b"id",
            self.LinkRole: b"lien",
            self.TypeRole: b"type",
            self.PromptRole: b"prompt",
            self.LienIARole: b"lienIA",
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

    @Slot(str, str, str, str)
    def addMediaItem(self, id, file_path, media_type, prompt="", lienIA=""):
        """
        Add a new media item to the model.

        :param id: int
        :param file_path: str
        :param media_type: str
        :param prompt: str
        :param lienIA: str
        :return: None
        """
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append({"id": id, "lien": file_path,
                           "type": media_type, "prompt": prompt, "lienIA": lienIA})
        self.endInsertRows()

    def updateMediaItem(self, id, file_path=None, file_path_ia=None, media_type=None, prompt=None):
        """
        Update an existing media item in the model.

        :param id: int
        :param file_path: str
        :param file_path_ia: str
        :param media_type: str
        :param prompt: str
        :return: None
        """
        for row in self._items:
            if row["id"] == id:
                if file_path:
                    row["lien"] = file_path
                if file_path_ia:
                    row["lienIA"] = file_path_ia
                if media_type:
                    row["type"] = media_type
                if prompt:
                    row["prompt"] = prompt
                self.dataChanged.emit(self.index(
                    row["index"]), self.index(row["index"]))
                break


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
            cursor.execute(
                "SELECT id, lien, type, prompt, lienIA FROM MediaData")
            rows = cursor.fetchall()

            # Convert data to dictionaries for the model
            data = [{"id": row[0], "lien": row[1], "type": row[2], "prompt": row[3]
                     if row[3] else "", "lienIA": row[4] if row[4] else ""} for row in rows]
            self._media_model.update_data(data)  # Update the media model

            self.dataLoaded.emit()  # Emit the signal to indicate data has been loaded

        except sqlite3.Error as e:
            print(f"Error accessing the database: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(str, str, str, str)
    def addMediaItem(self, file_path, media_type):
        """
        Add a new media item to the model and insert it into the database.

        :param file_path: str
        :param media_type: str
        :return: int
        """
        id_row = self.insert_into_database(
            file_path=file_path, media_type=media_type)
        self._media_model.addMediaItem(id_row, file_path, media_type)
        return id_row

    @Slot(int, str, str, str, str)
    def updateMediaItem(self, id, file_path=None, file_path_ia=None, media_type=None, prompt=None):
        """
        Update an existing media item in the model and database.

        :param id: int
        :param file_path: str
        :param file_path_ia: str
        :param media_type: str
        :param prompt: str
        :return: None
        """
        self._media_model.updateMediaItem(
            id, file_path, file_path_ia, media_type, prompt)
        self.insert_into_database(
            file_path=file_path, lienIA=file_path_ia, media_type=media_type, prompt=prompt, id_row=id)

    def insert_into_database(self, file_path=None, media_type=None, prompt=None, lienIA=None, id_row=None):
        """
        Insert or update a new media item into the database.

        :param file_path: str
        :param media_type: str
        :param prompt: str
        :param lienIA: str
        :return: None
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            fields = {
                "lien": file_path,
                "type": media_type,
                "prompt": prompt,
                "lienIA": lienIA
            }

            if id_row:
                update_fields = [f"{key} = ?" for key,
                                 value in fields.items() if value is not None]
                update_values = [
                    value for value in fields.values() if value is not None]
                update_values.append(id_row)
                cursor.execute(f"UPDATE MediaData SET {', '.join(
                    update_fields)} WHERE id = ?", update_values)
            else:
                insert_fields = [key for key,
                                 value in fields.items() if value is not None]
                insert_values = [
                    value for value in fields.values() if value is not None]
                cursor.execute(f"INSERT INTO MediaData ({', '.join(insert_fields)}) VALUES ({
                               ', '.join(['?'] * len(insert_values))})", insert_values)
                id_row = cursor.lastrowid
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting into the database: {e}")
        finally:
            if connection:
                connection.close()
        return id_row

    @Slot(result=dict)
    def get_last_media(self):
        """
        Retrieve the last recorded media item from the database.

        :return: dict
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, lien, type, prompt, lienIA FROM MediaData ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "lien": row[1], "type": row[2], "prompt": row[3], "lienIA": row[4]}
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
