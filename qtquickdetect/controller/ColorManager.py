import sys
import json
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication


class ColorManager(QObject):
    themeChanged = Signal()

    def __init__(self, theme_file, theme):
        super().__init__()
        with open(theme_file, 'r') as f:
            self.themes = json.load(f)
        self.current_theme = theme
        self.colors = self.themes[self.current_theme]

    @Property("QVariant", notify=themeChanged)
    def getColor(self):
        return self.colors
    
    @Slot()
    def switchTheme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.colors = self.themes[self.current_theme]
        self.themeChanged.emit()