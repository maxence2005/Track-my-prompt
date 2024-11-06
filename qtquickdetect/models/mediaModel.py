import sqlite3
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

class MediaModel(QAbstractListModel):
    # Définit les rôles des éléments de modèle
    LinkRole = Qt.UserRole + 1
    TypeRole = Qt.UserRole + 2
    PromptRole = Qt.UserRole + 3

    def __init__(self, *args, **kwargs):
        super(MediaModel, self).__init__(*args, **kwargs)
        self._items = []

    def data(self, index, role):
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
        return len(self._items)

    def roleNames(self):
        # Mappe les rôles aux noms de propriété pour les utiliser dans QML
        return {
            self.LinkRole: b"lien",
            self.TypeRole: b"type",
            self.PromptRole: b"prompt",
        }

    def update_data(self, data):
        # Remplace les données actuelles du modèle par de nouvelles données
        self.beginResetModel()
        self._items = data
        self.endResetModel()

    @Slot(str, str, str)
    def addMediaItem(self, file_path, media_type, prompt=""):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append({"lien": file_path, "type": media_type, "prompt": prompt})
        self.endInsertRows()
    



class DatabaseManagerMedia(QObject):
    dataLoaded = Signal()

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self._media_model = MediaModel()
        self.load_data()

    @Slot()
    def load_data(self):
        # Charge les données de la base de données
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT lien, type, prompt FROM MediaData")
            rows = cursor.fetchall()

            # Convertit les données en dictionnaires pour le modèle
            data = [{"lien": row[0], "type": row[1], "prompt": row[2] if row[2] else ""} for row in rows]
            self._media_model.update_data(data)  # Correction : mise à jour du modèle média

            self.dataLoaded.emit()  # Emit the signal to indicate data has been loaded

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(str, str, str)
    def addMediaItem(self, file_path, media_type, prompt=""):
        self._media_model.addMediaItem(file_path, media_type, prompt)
        self.insert_into_database(file_path, media_type, prompt)

    def insert_into_database(self, file_path, media_type, prompt):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Utilisation d'une requête préparée pour éviter les injections SQL
            cursor.execute("INSERT INTO MediaData (lien, type, prompt) VALUES (?, ?, ?)", 
                           (file_path, media_type, prompt))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion dans la base de données: {e}")
        finally:
            if connection:
                connection.close()

    @Slot(result=dict)
    def get_last_media(self):
        # Récupère le dernier média enregistré
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT lien, type, prompt FROM MediaData ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                return {"lien": row[0], "type": row[1], "prompt": row[2]}
            else:
                return {}  # Retourne un dictionnaire vide si aucun média trouvé
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du dernier média: {e}")
            return {}
        finally:
            if connection:
                connection.close()

    @Slot()
    def clear_all_media(self):
        # Supprime tous les enregistrements de la table MediaData
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM MediaData")
            connection.commit()
            # Met à jour le modèle pour refléter la suppression
            self._media_model.update_data([])
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression des médias: {e}")
        finally:
            if connection:
                connection.close()

    @Property(QObject, constant=True)
    def mediaModel(self):
        """Expose mediaModel à QML."""
        return self._media_model
