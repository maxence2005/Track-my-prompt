import sqlite3
from PySide6.QtCore import QTimer, QObject, Signal, Slot, Property, QAbstractListModel, QModelIndex, Qt

class HistoriqueModel(QAbstractListModel):
    """
    Model to handle the history data for the QML view.
    """
    PromptRole = Qt.UserRole + 1
    IDRole = Qt.UserRole + 2
    PageIDRole = Qt.UserRole + 3
    DateCreationRole = Qt.UserRole + 4
    LienRole = Qt.UserRole + 5
    TypeRole = Qt.UserRole + 6
    LienIARole = Qt.UserRole + 7
    TitreCaseRole = Qt.UserRole + 8  

    def __init__(self, *args, **kwargs):
        """
        Initialize the model.
        """
        super(HistoriqueModel, self).__init__(*args, **kwargs)
        self._items = []  # Liste pour stocker les éléments du modèle
        self.current_pageID = None  # Variable pour stocker le pageID actuel

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
        elif role == self.IDRole:
            return item["id"]
        elif role == self.PageIDRole:
            return item["pageID"]
        elif role == self.DateCreationRole:
            return item["date_creation"]
        elif role == self.LienRole:
            return item["lien"]
        elif role == self.TypeRole:
            return item["type"]
        elif role == self.LienIARole:
            return item["lienIA"]
        elif role == self.TitreCaseRole:
            return item["titre_case"]

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
            self.IDRole: b"id",
            self.PageIDRole: b"pageID",
            self.DateCreationRole: b"date_creation",
            self.LienRole: b"lien",
            self.TypeRole: b"type",
            self.LienIARole: b"lienIA",
            self.TitreCaseRole: b"titre_case"
        }

    def add_item(self, item):
        """Ajoute un élément au modèle uniquement si le pageID est unique."""
        pageID = item["pageID"]

        # Vérifier si un élément avec ce pageID existe déjà
        if self.has_pageID(pageID):
            print(f"Le pageID {pageID} existe déjà, l'élément est ignoré.")
            return  # Ne pas ajouter l'élément si le pageID existe déjà

        # Ajouter l'élément à la liste si le pageID est unique
        self.beginInsertRows(QModelIndex(), 0, 0)
        self._items.insert(0, item)
        self.endInsertRows()
        self.dataChanged.emit(self.index(len(self._items) - 1), self.index(len(self._items) - 1), [self.PromptRole])
        print(f"Élément avec pageID {pageID} ajouté au modèle.")


    def update_items_by_pageID(self, pageID, newText):
        """Met à jour le texte des éléments ayant le même `pageID`."""
        for index, item in enumerate(self._items):
            if item["pageID"] == pageID:
                self._items[index]["prompt"] = newText

        # On émet un signal pour informer que les données ont changé
        self.dataChanged.emit(self.index(0), self.index(len(self._items) - 1), [self.PromptRole])

    def remove_items_by_pageID(self, pageID):
        """Supprime tous les éléments ayant un `pageID` donné."""
        rows_to_remove = [i for i, item in enumerate(self._items) if item["pageID"] == pageID]
        for row in reversed(rows_to_remove):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._items[row]
            self.endRemoveRows()

    def add_data_if_new_pageID(self, data):
        """Ajoute des éléments si le `pageID` est nouveau, mais seulement le premier élément rencontré."""
        if not data or not isinstance(data, list):
            return  # Aucune donnée ou mauvais format

        try:
            new_pageID = data[0]["pageID"]
        except (IndexError, KeyError) as e:
            print(f"Erreur : impossible de récupérer le pageID. Vérifiez vos données. {e}")
            return

        # Si le pageID est déjà dans le modèle, on ignore l'ajout
        if self.has_pageID(new_pageID):
            print(f"Le pageID {new_pageID} existe déjà. Données ignorées.")
            return

        # Si on est ici, cela signifie que le pageID est nouveau, donc on ajoute seulement le premier élément
        print(f"Ajout des données pour le nouveau pageID {new_pageID}.")
        
        # On ajoute uniquement le premier élément de la liste de données
        first_item = data[0]  # Récupère uniquement le premier élément

        # On ajoute le premier élément au modèle
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append(first_item)
        self.endInsertRows()

        print(f"Premier élément ajouté pour le pageID {new_pageID}: {first_item}")


    def has_pageID(self, pageID):
        """Vérifie si le `pageID` existe déjà dans le modèle."""
        return any(item["pageID"] == pageID for item in self._items)

    def remove_item_by_id(self, idToDelete):
        """Supprime un élément par son `id`."""
        index_to_delete = next((index for index, item in enumerate(self._items) if item["id"] == idToDelete), None)

        if index_to_delete is not None:
            self.beginRemoveRows(QModelIndex(), index_to_delete, index_to_delete)
            del self._items[index_to_delete]
            self.endRemoveRows()
        else:
            print(f"Élément avec id {idToDelete} non trouvé.")

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
            cursor.execute("SELECT id, pageID, date_creation, lien, type, prompt, lienIA, titre_case FROM Historique")
            rows = cursor.fetchall()

            data_by_page = {}
            for row in rows:
                try:
                    pageID = row[1]  
                    if pageID is None:
                        raise ValueError(f"Entrée avec un pageID invalide détectée : {row}")

                    if pageID not in data_by_page:
                        data_by_page[pageID] = []
                    data_by_page[pageID].append({
                        "id": row[0],
                        "pageID": pageID,
                        "date_creation": row[2],
                        "lien": row[3],
                        "type": row[4],
                        "prompt": row[5],
                        "lienIA": row[6],
                        "titre_case": row[7],
                    })
                except Exception as e:
                    print(f"Erreur lors du traitement de la ligne {row}: {e}")
                    continue  

            for pageID in sorted(data_by_page.keys(), reverse=True):
                data = data_by_page[pageID]
                self.historique_model.add_data_if_new_pageID(data)
                print(f"Historique chargé pour pageID {pageID} avec {len(data)} éléments")

        except sqlite3.Error as e:
            print(f"Erreur lors de l'accès à la base de données: {e}")
            raise
        finally:
            if connection:
                connection.close()

    def remove_items_from_model(self, idToDelete):
        self.historique_model.remove_items_by_pageID(idToDelete)

    def update_items_by_pageID(self, pageID, newText):
        """Met à jour les éléments ayant le même pageID dans le modèle."""
        self.historique_model.update_items_by_pageID(pageID, newText)

    def add_item(self, item, pageID):
        """Ajoute un élément dans le modèle si le pageID est nouveau."""
        self.historique_model.add_item(item)

    def add_entry(self, pageID, prompt, lien, media_type, lienIA, titre_case) -> int:
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO Historique (pageID, prompt, lien, type, lienIA,titre_case)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (pageID, prompt, lienIA, media_type, lien, titre_case)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

    def update_lienIA(self, id_elem, new_lienIA):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE Historique SET lien = ? WHERE id = ?",
                (new_lienIA, id_elem)
            )
            connection.commit()
        finally:
            connection.close()

    def delete_by_pageID(self, pageID):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Historique WHERE pageID = ?", (pageID,))
            connection.commit()
        finally:
            connection.close()

    def modify_prompt(self, pageID, new_prompt):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE Historique SET prompt = ? WHERE pageID = ?", (new_prompt, pageID))
            connection.commit()
        finally:
            connection.close()

    def get_max_pageID(self) -> int:
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(pageID) FROM Historique")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
        finally:
            connection.close()

    def page_exists(self, pageID: int) -> bool:
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Historique WHERE pageID = ?", (pageID,))
            return cursor.fetchone()[0] > 0
        finally:
            connection.close()

    def get_entries_by_pageID(self, pageID):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id, prompt, lien, type, lienIA FROM Historique WHERE pageID = ?", (pageID,))
            return cursor.fetchall()
        finally:
            connection.close()

    def update_case_title(self, pageID: int, new_title: str):
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE Historique SET titre_case = ? WHERE pageID = ?", (new_title, pageID))
            connection.commit()
        finally:
            connection.close()

    def get_case_title(self, pageID: int) -> str:
        connection = sqlite3.connect(self.db_path)
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT titre_case FROM Historique WHERE pageID = ? LIMIT 1", (pageID,))
            row = cursor.fetchone()
            return row[0] if row and row[0] else ""
        finally:
            connection.close()


    @Property(QObject, constant=True)
    def historiqueModel(self) -> HistoriqueModel:
        """
        Exposes the model to the QML view.
        
        :return: HistoriqueModel
        """
        return self.historique_model
