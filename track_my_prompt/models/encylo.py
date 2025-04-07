import sqlite3
import os
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt
import copy
from utils import filepaths

class EncyclopediaModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    EmoticonRole = Qt.UserRole + 2
    TimeFoundRole = Qt.UserRole + 3

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EncyclopediaModel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self._initialized:
            super(EncyclopediaModel, self).__init__(*args, **kwargs)
            self._items_base = []
            self._items = []
            self._all_items = []
            self._initialized = True
    
    @staticmethod
    def get_instance() -> 'EncyclopediaModel':
        """
        Get the singleton instance of the EncyclopediaModel.

        Returns:
            EncyclopediaModel: The singleton instance.
        """
        return EncyclopediaModel()
    
    def data(self, index: QModelIndex, role: int):
        """
        Get the data for the given index and role.

        Args:
            index (QModelIndex): The index of the item.
            role (int): The role for which data is requested.

        Returns:
            Any: The data for the given index and role.
        """
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]
        if role == self.NameRole:
            return item["englishName"]
        elif role == self.EmoticonRole:
            return item["emoticon"]
        elif role == self.TimeFoundRole:
            return item["timeFound"]

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Get the number of rows in the model.

        Args:
            parent (QModelIndex): The parent index.

        Returns:
            int: The number of rows in the model.
        """
        return len(self._items)

    def roleNames(self) -> dict:
        """
        Get the role names for the model.

        Returns:
            dict: A dictionary mapping role numbers to role names.
        """
        return {
            self.NameRole: b"englishName",
            self.EmoticonRole: b"emoticon",
            self.TimeFoundRole: b"timeFound",
        }


    def filter_data(self, search_text: str):
        """
        Filter the data based on the search text.

        Args:
            search_text (str): The text to filter the data by.
        """
        if not search_text:
            self.update_data_bis(self._all_items)
        else:
            filtered_items = [
                item for item in self._all_items
                if search_text.lower() in item["englishName"].lower()
            ]
            self.update_data_bis(filtered_items)

    def initialize_data(self, data: list):
        """
        Initialize the model with the given data.

        Args:
            data (list): The data to initialize the model with.
        """
        self.beginResetModel()
        self._items_base = copy.deepcopy(data)
        self._items = data
        self._all_items = data
        self.endResetModel()

    def update_data(self, data: list):
        """
        Update the model with the given data.

        Args:
            data (list): The data to update the model with.
        """
        self.beginResetModel()
        self._items = data
        self._all_items = data
        self.endResetModel()

    def update_data_bis(self, data: list):
        """
        Update the model with the given data without changing the base items.

        Args:
            data (list): The data to update the model with.
        """
        self.beginResetModel()
        self._items = data
        self.endResetModel()
    
    def changeName(self, newDict: dict):
        """
        Changes the english name to the new name given by the parameter newDict.

        Args:
            newDict (dict): A dictionary containing the new names.
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
        Restores the original english name in the encyclopedia.
        """
        for i in range(len(self._items_base)):
            self._all_items[i]["englishName"] = self._items_base[i]["englishName"]
            index = self.index(i)
            self.dataChanged.emit(index, index, [self.NameRole])
        self.update_data_bis(self._all_items)

    def get_all_names(self) -> set:
        """
        Get all the english names in the encyclopedia.

        Returns:
            set: A set of all the english names.
        """
        return {item["englishName"] for item in self._all_items}
    
    def changeTimeFound(self, dict: dict):
        """
        Updates the time found in the database.

        Args:
            dict (dict): A dictionary containing the new times found.
        """
        for name, timeFound in dict.items():
            for i in range(len(self._items_base)):
                if self._items_base[i]["englishName"] == name:
                    self._all_items[i]["timeFound"] = timeFound
                    index = self.index(i)
                    self.dataChanged.emit(index, index, [self.TimeFoundRole])
                    break
        self.update_data_bis(self._all_items)

    def incrementTimeFound(self, classes: list):
        """
        Increments the number of times the classes were found by 1.

        Args:
            classes (list): The classes to update.
        """
        db_path = os.path.join(filepaths.get_base_data_dir(), 'trackmyprompt.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        dict = {}
        for obj in classes:
            rows = cursor.execute(f"SELECT timeFound FROM Encyclopedie WHERE englishName = ?", [obj]).fetchone()
            val = rows[0]
            val += 1
            cursor.execute(f"UPDATE Encyclopedie SET timeFound = ? WHERE englishName = ?", [val,obj])
            dict[obj] = val
        connection.commit()
        connection.close()

        self.changeTimeFound(dict)
    
    def getPourcentFound(self)->float:
        """
        Get the percentage of items found in the encyclopedia.

        Returns:
            float: The percentage of items found.
        """
        cpt = 0
        for item in self._all_items:
            if item["timeFound"] > 0:
                cpt += 1
        return cpt/len(self._all_items)
        

class DatabaseManager(QObject):
    
    dataLoaded = Signal()

    def __init__(self, db_path: str, parent: QObject = None):
        """
        Initialize the DatabaseManager with the given database path.

        Args:
            db_path (str): The path to the database file.
            parent (QObject, optional): The parent object. Defaults to None.
        """
        super().__init__(parent)
        self.db_path = db_path
        self.model = EncyclopediaModel.get_instance()
        self.load_data()

    @Slot()
    def load_data(self):
        """
        Loads the encyclopedia data from the database.
        """
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT englishName, emoticon, timeFound FROM Encyclopedie")
            rows = cursor.fetchall()

            data = [{"englishName": row[0], "emoticon": row[1], "timeFound": row[2]} for row in rows]

            self.model.initialize_data(data)
            self.dataLoaded.emit()

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
            raise
        finally:
            if connection:
                connection.close()
    
    @Slot(str)
    def set_search_text(self, text: str):
        """
        Updates the filter in the model.

        Args:
            text (str): The text to filter the data by.
        """
        self.model.filter_data(text)

    @Property(QObject, constant=True)
    def encyclopediaModel(self) -> QObject:
        """
        Exposes the model to the QML view.

        Returns:
            QObject: The encyclopedia model.
        """
        return self.model
    
    @Slot(result="double")
    def pourcentFound(self)->float:
        """
        Get the percentage of items found in the encyclopedia.

        Returns:
            float: The percentage of items found.
        """
        return self.model.getPourcentFound()