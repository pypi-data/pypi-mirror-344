"""Model for chips widget"""

from abc import abstractmethod, ABC

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from jb_qt.models.chip_button import IChipButton


class IChipsWidget(QWidget):
    """ChipsWidget model"""

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

    def add_chip(self):
        pass

    def remove_chip(self, button: IChipButton):
        pass

    def add_chips(self, items: list[str]) -> None:
        pass

    def remove_chips(self, items: list[str]) -> None:
        pass

    def remove_all(self, *_) -> None:
        pass
