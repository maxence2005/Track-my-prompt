import sqlite3
import os
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

class HistoriqueModel(QAbstractListModel):
    """
    Model to handle the history data for the QML view.
    """
    PromptRole = Qt.UserRole + 1

    def __init__(self, *args, **kwargs):
        """
        Initialize the model.
        """
        super(HistoriqueModel, self).__init__(*args, **kwargs)
        self._items = []

    def data(self, index: QModelIndex, role: int) -> str:
        """
        Get data for the given index and role.
        
        :param index: QModelIndex
        :param role: int
        :return: str
        """
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]
        if role == self.PromptRole:
            return item["prompt"]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Get the number of rows in the model.
        
        :param parent: QModelIndex
        :return: int
        """
        return len(self._items)

    def roleNames(self) -> dict:
        """
        Get the role names for the model.
        
        :return: dict
        """
        return {
            self.PromptRole: b"prompt",
        }

    def update_data(self, data: list) -> None:
        """
        Update the model data.
        
        :param data: list
        """
        self.beginResetModel()
        self._items = data
        self.endResetModel()

class DatabaseManagerHistorique(QObject):
    """
    Manager to handle database operations for the history data.
    """
    historiqueDataLoaded = Signal()

    def __init__(self, db_path: str, parent: QObject = None) -> None:
        """
        Initialize the database manager.
        
        :param db_path: str
        :param parent: QObject
        """
        super().__init__(parent)
        self.db_path = db_path
        self.historique_model = HistoriqueModel()
        self.load_historique_data()

    @Slot()
    def load_historique_data(self) -> None:
        """
        Loads the history data from the database.
        """
        connection = None
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT prompt FROM Historique")
            rows = cursor.fetchall()

            data = [{"prompt": row[0]} for row in rows]

            self.historique_model.update_data(data)
            self.historiqueDataLoaded.emit()

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
            raise
        finally:
            if connection:
                connection.close()

    @Property(QObject, constant=True)
    def historiqueModel(self) -> HistoriqueModel:
        """
        Exposes the model to the QML view.
        
        :return: HistoriqueModel
        """
        return self.historique_model
