import sqlite3
import os
from PySide6.QtCore import QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

# Définir le modèle QML pour les éléments de l'historique
class HistoriqueModel(QAbstractListModel):
    PromptRole = Qt.UserRole + 1

    def __init__(self, *args, **kwargs):
        super(HistoriqueModel, self).__init__(*args, **kwargs)
        self._items = []

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self._items)):
            return None

        item = self._items[index.row()]
        if role == self.PromptRole:
            return item["prompt"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def roleNames(self):
        return {
            self.PromptRole: b"prompt",
        }

    def update_data(self, data):
        self.beginResetModel()
        self._items = data
        self.endResetModel()

class DatabaseManagerHistorique(QObject):

    historiqueDataLoaded = Signal()

    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.historique_model = HistoriqueModel()
        self.load_historique_data()

    @Slot()
    def load_historique_data(self):
        connection = None
        # Charge les données de l'historique depuis la base de données
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT prompt FROM Historique")
            rows = cursor.fetchall()

            data = [{"prompt": row[0]} for row in rows]

            # Met à jour le modèle Historique
            self.historique_model.update_data(data)
            self.historiqueDataLoaded.emit()

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
            raise
        finally:
            if connection:
                connection.close()

    @Property(QObject, constant=True)
    def historiqueModel(self):
        """Expose le modèle Historique à QML"""
        return self.historique_model
