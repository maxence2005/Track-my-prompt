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

    def data(self, index: QModelIndex, role: int):
        """
        Retrieve data for the given index and role.

        Args:
            index (QModelIndex): The index of the item.
            role (int): The role of the data.

        Returns:
            Any: The data corresponding to the role.
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

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Return the number of rows in the model.

        Args:
            parent (QModelIndex, optional): The parent index. Defaults to QModelIndex().

        Returns:
            int: The number of rows.
        """
        return len(self._items)

    def roleNames(self) -> dict:
        """
        Map roles to property names for use in QML.

        Returns:
            dict: The role names.
        """
        return {
            self.IdRole: b"id",
            self.LinkRole: b"lien",
            self.TypeRole: b"type",
            self.PromptRole: b"prompt",
            self.LienIARole: b"lienIA",
        }

    def update_data(self, data: list):
        """
        Replace the current model data with new data.

        Args:
            data (list): The new data.
        """
        self.beginResetModel()
        self._items = data
        self.endResetModel()

    @Slot(str, str, str, str)
    def addMediaItem(self, id: str, file_path: str, media_type: str, prompt: str = "", lienIA: str = ""):
        """
        Add a new media item to the model.

        Args:
            id (str): The ID of the media item.
            file_path (str): The file path of the media item.
            media_type (str): The type of the media item.
            prompt (str, optional): The prompt associated with the media item. Defaults to "".
            lienIA (str, optional): The IA link associated with the media item. Defaults to "".
        """
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append({"id": id, "lien": file_path,
                           "type": media_type, "prompt": prompt, "lienIA": lienIA})
        self.endInsertRows()

    def updateMediaItem(self, id: str, file_path: str = None, file_path_ia: str = None, media_type: str = None, prompt: str = None):
        """
        Update an existing media item in the model.

        Args:
            id (str): The ID of the media item.
            file_path (str, optional): The new file path. Defaults to None.
            file_path_ia (str, optional): The new IA link. Defaults to None.
            media_type (str, optional): The new media type. Defaults to None.
            prompt (str, optional): The new prompt. Defaults to None.
        """
        print(f"Début de mise à jour de l'élément média avec ID : {id}")
        found = False

        for i, row in enumerate(self._items):
            print(f"[DEBUG] Vérification de l'élément : {row}")
            if row["id"] == id:
                found = True
                print(f"[DEBUG] État initial de l'élément : {row}")
                if file_path:
                    print(f"[DEBUG] Mise à jour de 'lien' avec : {file_path}")
                    row["lien"] = file_path
                if file_path_ia:
                    print(f"[DEBUG] Mise à jour de 'lienIA' avec : {file_path_ia}")
                    row["lienIA"] = file_path_ia
                if media_type:
                    print(f"[DEBUG] Mise à jour de 'type' avec : {media_type}")
                    row["type"] = media_type
                if prompt:
                    print(f"[DEBUG] Mise à jour de 'prompt' avec : {prompt}")
                    row["prompt"] = prompt
                print(f"[DEBUG] État mis à jour de l'élément : {row}")
                self.dataChanged.emit(self.index(i), self.index(i))
                break
        
        if not found:
            print(f"[ERREUR] Aucun élément trouvé avec l'ID : {id}")


class DatabaseManagerMedia(QObject):
    """
    DatabaseManagerMedia handles database operations and manages the MediaModel.
    """
    dataLoaded = Signal()

    def __init__(self, db_path: str, parent: QObject = None):
        """
        Initialize the DatabaseManagerMedia.

        Args:
            db_path (str): The path to the database.
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self.db_path = db_path
        self._media_model = MediaModel()
        self.load_data()

    @Slot()
    def load_data(self):
        """
        Load data from the database and update the media model.
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

    @Slot(str, str)
    def addMediaItem(self, file_path: str, media_type: str) -> int:
        """
        Add a new media item to the model and insert it into the database.

        Args:
            file_path (str): The file path of the media item.
            media_type (str): The type of the media item.

        Returns:
            int: The ID of the new media item.
        """
        id_row = self.insert_into_database(
            file_path=file_path, media_type=media_type)
        self._media_model.addMediaItem(id_row, file_path, media_type)
        return id_row

    @Slot(int, str, str, str, str)
    def updateMediaItem(self, id: int, file_path: str = None, file_path_ia: str = None, media_type: str = None, prompt: str = None):
        """
        Update an existing media item in the model and database.

        Args:
            id (int): The ID of the media item.
            file_path (str, optional): The new file path. Defaults to None.
            file_path_ia (str, optional): The new IA link. Defaults to None.
            media_type (str, optional): The new media type. Defaults to None.
            prompt (str, optional): The new prompt. Defaults to None.
        """
        print(f"voici l'id dans le premier updateMedia : {id}")
        self._media_model.updateMediaItem(
            id, file_path, file_path_ia, media_type, prompt)
        self.insert_into_database(
            file_path=file_path, lienIA=file_path_ia, media_type=media_type, prompt=prompt, id_row=id)

    def insert_into_database(self, file_path: str = None, media_type: str = None, prompt: str = None, lienIA: str = None, id_row: int = None) -> int:
        """
        Insert or update a new media item into the database.

        Args:
            file_path (str, optional): The file path of the media item. Defaults to None.
            media_type (str, optional): The type of the media item. Defaults to None.
            prompt (str, optional): The prompt associated with the media item. Defaults to None.
            lienIA (str, optional): The IA link associated with the media item. Defaults to None.
            id_row (int, optional): The ID of the media item. Defaults to None.

        Returns:
            int: The ID of the media item.
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
                cursor.execute(f"UPDATE MediaData SET {', '.join(update_fields)} WHERE id = ?", update_values)
            else:
                insert_fields = [key for key,
                                 value in fields.items() if value is not None]
                insert_values = [
                    value for value in fields.values() if value is not None]
                cursor.execute(f"INSERT INTO MediaData ({', '.join(insert_fields)}) VALUES ({', '.join(['?'] * len(insert_values))})", insert_values)
                id_row = cursor.lastrowid
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting into the database: {e}")
        finally:
            if connection:
                connection.close()
        return id_row

    @Slot(result=dict)
    def get_last_media(self) -> dict:
        """
        Retrieve the last recorded media item from the database.

        Returns:
            dict: The last recorded media item.
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
                return {}  # Returns an empty dictionary if no media found
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
        """
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM MediaData")
            connection.commit()
            # Updates the model to reflect the deletion
            self._media_model.update_data([])
        except sqlite3.Error as e:
            print(f"Error deleting media: {e}")
        finally:
            if connection:
                connection.close()

    @Property(QObject, constant=True)
    def mediaModel(self) -> MediaModel:
        """
        Expose mediaModel to QML.

        Returns:
            MediaModel: The media model.
        """
        return self._media_model
