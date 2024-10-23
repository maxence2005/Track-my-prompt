import sys
from PySide6.QtCore import QObject, Slot, Signal, QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

class Backend(QObject):
    # Déclarez un signal
    infoSent = Signal(str)

    @Slot(str)
    def receivePrompt(self, promptText):
        print(f"Received prompt: {promptText}")
        # Traitez le texte ici
        # Émettez le signal avec les informations
        self.infoSent.emit(f"Processed: {promptText}")

def main():
    # Créer une instance d'application Qt
    app = QApplication(sys.argv)

    # Créer une instance du backend
    backend = Backend()

    # Créer une instance de QQmlApplicationEngine
    engine = QQmlApplicationEngine()

    # Exposer le backend au contexte QML
    engine.rootContext().setContextProperty("backend", backend)

    # Charger le fichier QML
    engine.load(QUrl("App.qml"))

    # Vérifier si le fichier QML est chargé correctement
    if not engine.rootObjects():
        sys.exit(-1)

    # Lancer la boucle d'événements de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()