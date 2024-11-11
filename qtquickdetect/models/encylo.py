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
        self._items_base = []
        self._items = []
        self._all_items = []

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


    def filter_data(self, search_text):
        if not search_text:
            self.update_data_bis(self._all_items)
        else:
            filtered_items = [
                item for item in self._all_items
                if search_text.lower() in item["englishName"].lower()
            ]
            self.update_data_bis(filtered_items)

    def initialize_data(self, data):
        self.beginResetModel()
        self._items_base = data
        self._items = data
        self._all_items = data
        self.endResetModel()

    def update_data(self, data):
        self.beginResetModel()
        self._items = data
        self._all_items = data
        self.endResetModel()

    def update_data_bis(self, data):
        self.beginResetModel()
        self._items = data
        self.endResetModel()
    
    def changeName(self, newDict):
        """
        Change le nom anglais de l'élément de l'encyclopédie par un autre nom donné dans newDict.
        Structure de newDict: {"oldName": "newName", "oldName2": "newName2", ...}

        Args:
            newDict (dict): Dictionnaire contenant les anciens noms et les nouveaux noms.
        """
        for oldName, newName in newDict.items():
            for i in range(len(self._items_base)):
                if self._items_base[i]["englishName"] == oldName:
                    self._items[i]["englishName"] = newName
                    index = self.index(i)
                    self.dataChanged.emit(index, index, [self.NameRole])
                    break
        self.update_data_bis(self._items)
        self.update_data_bis(self._all_items)
    
    def restoreName(self):
        """
        Restaure le nom anglais de l'élément de l'encyclopédie à son nom original.
        """
        for i in range(len(self._items_base)):
            self._items[i]["englishName"] = self._items_base[i]["englishName"]
            index = self.index(i)
            self.dataChanged.emit(index, index, [self.NameRole])
        self.update_data_bis(self._items_base)
        self.update_data_bis(self._all_items)
    

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
            self.model.initialize_data(data)
            self.dataLoaded.emit()
            # Debug: afficher le contenu du modèle

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
        finally:
            if connection:
                connection.close()
    
    @Slot(str)
    def set_search_text(self, text):
        """Met à jour la recherche dans le modèle."""
        self.model.filter_data(text)

    @Property(QObject, constant=True)
    def encyclopediaModel(self):
        """Expose le modèle à QML"""
        return self.model