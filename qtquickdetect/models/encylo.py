import sqlite3
import os
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt
import copy
from utils import filepaths

# Définir le modèle QML pour les éléments de l'encyclopédie
class EncyclopediaModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    EmoticonRole = Qt.UserRole + 2
    TimeFoundRole = Qt.UserRole + 3

    _instance = None  # Attribut de classe pour stocker l'instance unique
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EncyclopediaModel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        # L'initialisation réelle ne doit s'exécuter qu'une seule fois
        if not self._initialized:
            super(EncyclopediaModel, self).__init__(*args, **kwargs)
            self._items_base = []
            self._items = []
            self._all_items = []
            self._initialized = True
    
    @staticmethod
    def get_instance() -> 'EncyclopediaModel':
        return EncyclopediaModel()
    
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
        self._items_base = copy.deepcopy(data)
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
                    self._all_items[i]["englishName"] = newName
                    index = self.index(i)
                    self.dataChanged.emit(index, index, [self.NameRole])
                    break
        self.update_data_bis(self._all_items)
    
    def restoreName(self):
        """
        Restaure le nom anglais de l'élément de l'encyclopédie à son nom original.
        """
        for i in range(len(self._items_base)):
            self._all_items[i]["englishName"] = self._items_base[i]["englishName"]
            index = self.index(i)
            self.dataChanged.emit(index, index, [self.NameRole])
        self.update_data_bis(self._all_items)

    def get_all_names(self):
        return {item["englishName"] for item in self._all_items}
    
    def changeTimeFound(self, dict):
        print("Change time found :")
        print(dict)
        for name, timeFound in dict.items():
            print(len(self._items_base))
            for i in range(len(self._items_base)):
                print("coucou")
                if self._items_base[i]["englishName"] == name:
                    self._all_items[i]["timeFound"] = timeFound
                    index = self.index(i)
                    self.dataChanged.emit(index, index, [self.TimeFoundRole])
                    break
        self.update_data_bis(self._all_items)

    def incrementTimeFound(self, classes):
        db_path = os.path.join(filepaths.get_base_data_dir(), 'trackmyprompt.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        dict = {}
        print("increment time found")
        print(self._items)
        print(self._items_base)
        print(self._all_items)
        for obj in classes:
            rows = cursor.execute(f"SELECT timeFound FROM Encyclopedie WHERE englishName = ?", [obj]).fetchone()
            val = rows[0]
            val += 1
            cursor.execute(f"UPDATE Encyclopedie SET timeFound = ? WHERE englishName = ?", [val,obj])
            dict[obj] = val
        connection.commit()
        connection.close()

        self.changeTimeFound(dict)

class DatabaseManager(QObject):
    
    dataLoaded = Signal()

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.model = EncyclopediaModel.get_instance()
        self.load_data()

    @Slot()
    def load_data(self):
        connection = None
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
            raise
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