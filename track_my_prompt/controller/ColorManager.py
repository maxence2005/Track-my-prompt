import sys
import json
from PySide6.QtCore import QUrl, QObject, Signal, Slot, Property, QPropertyAnimation
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication


class ColorManager(QObject):
    """
    ColorManager class to manage the application's color themes.
    """
    themeChanged = Signal()
    animations = []

    def __init__(self, theme_file: str, theme: str):
        """
        Initialize the ColorManager with the given theme file and initial theme.

        Args:
            theme_file (str): Path to the theme file.
            theme (str): Initial theme.
        """
        super().__init__()
        with open(theme_file, 'r') as f:
            self.themes = json.load(f)
        self.current_theme = theme
        self.colors = self.themes[self.current_theme]

    @Property("QVariant", notify=themeChanged)
    def getColor(self) -> dict:
        """
        Get the current colors.

        Returns:
            dict: The current colors.
        """
        return self.colors
    
    @Slot(str, result="QVariant")
    def getColorNoNotify(self, key: str) -> str:
        """
        Get a specific color without emitting a signal.

        Args:
            key (str): The color key.

        Returns:
            str: The color value.
        """
        return self.colors[key]
    
    @Slot()
    def switchTheme(self):
        """
        Switch between light and dark themes.
        """
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.colors = self.themes[self.current_theme]
        self.themeChanged.emit()
    
    @Property(bool, notify=themeChanged)
    def isLightMode(self) -> bool:
        """
        Check if the current theme is light mode.

        Returns:
            bool: True if light mode, False otherwise.
        """
        return self.current_theme == "light"
    
    @Property(bool, notify=themeChanged)
    def isDarkMode(self) -> bool:
        """
        Check if the current theme is dark mode.

        Returns:
            bool: True if dark mode, False otherwise.
        """
        return self.current_theme == "dark"
    
    @Slot(list)
    def animateColorChange(self, targets: list):
        """
        Animate the color change for the given targets.

        Args:
            targets (list): List of targets to animate.
        """
        for target in targets:
            animation = QPropertyAnimation(target[0], target[1].encode('utf-8'))
            animation.setDuration(300)
            animation.setEndValue(self.colors.get(target[2], "#000000"))
            animation.finished.connect(lambda anim=animation: self.animations.remove(anim))
            self.animations.append(animation) 
            animation.start()