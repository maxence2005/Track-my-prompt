import sys
import json
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property, QPropertyAnimation
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication


class ColorManager(QObject):
    themeChanged = Signal()
    animations = []

    def __init__(self, theme_file, theme):
        super().__init__()
        with open(theme_file, 'r') as f:
            self.themes = json.load(f)
        self.current_theme = theme
        self.colors = self.themes[self.current_theme]

    @Property("QVariant", notify=themeChanged)
    def getColor(self):
        return self.colors
    
    @Slot(str, result="QVariant")
    def getColorNoNotify(self, key):
        return self.colors[key]
    
    @Slot()
    def switchTheme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.colors = self.themes[self.current_theme]
        self.themeChanged.emit()
    
    @Property(bool, notify=themeChanged)
    def isLightMode(self):
        return self.current_theme == "light"
    
    @Property(bool, notify=themeChanged)
    def isDarkMode(self):
        return self.current_theme == "dark"
    
    @Slot(list)
    def animateColorChange(self, targets):
        for target in targets:
            animation = QPropertyAnimation(target[0], target[1].encode('utf-8'))
            animation.setDuration(300)
            animation.setEndValue(self.colors.get(target[2], "#000000"))
            animation.finished.connect(lambda anim=animation: self.animations.remove(anim))
            self.animations.append(animation)  # Conserver la référence
            animation.start()