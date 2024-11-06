import sqlite3
import os
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

# Définir le modèle QML pour les éléments de l'encyclopédie
class EncyclopediaModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    EmoticonRole = Qt.UserRole + 2
    TimeFoundRole = Qt.UserRole + 3

    def __init__(self, *args, **kwargs):
        super(EncyclopediaModel, self).__init__(*args, **kwargs)
        self._items = []

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]
        if role == self.NameRole:
            return item["englishName"]
        elif role == self.EmoticonRole:
            return item["emoticon"]
        elif role == self.TimeFoundRole:
            return item["timeFound"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def roleNames(self):
        return {
            self.NameRole: b"englishName",
            self.EmoticonRole: b"emoticon",
            self.TimeFoundRole: b"timeFound",
        }

    def update_data(self, data):
        self.beginResetModel()
        self._items = data
        self.endResetModel()

class DatabaseManager(QObject):
    
    dataLoaded = Signal()

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.model = EncyclopediaModel()
        self.load_data()

    @Slot()
    def load_data(self):
        # Charge les données de la base de données
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT englishName, emoticon, timeFound FROM Encyclopedie")
            rows = cursor.fetchall()

            data = [{"englishName": row[0], "emoticon": row[1], "timeFound": row[2]} for row in rows]

            # Debug: afficher les données chargées

            # Met à jour le modèle
            self.model.update_data(data)
            self.dataLoaded.emit()
            # Debug: afficher le contenu du modèle

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
        finally:
            if connection:
                connection.close()
    


    @Property(QObject, constant=True)
    def encyclopediaModel(self):
        """Expose le modèle à QML"""
        return self.model
