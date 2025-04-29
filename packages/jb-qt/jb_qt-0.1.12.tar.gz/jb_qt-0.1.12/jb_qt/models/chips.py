"""Model for chips widget"""

from abc import abstractmethod, ABC

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget

from jb_qt.models.chip_button import IChipButton


class IChipsWidget(ABC, QWidget):
    def __init__(self, parent: QObject = None, chips: list = None) -> None:
        super().__init__(parent)
        self.values: list = chips or []

    @abstractmethod
    def add_chip(self):
        pass

    @abstractmethod
    def remove_chip(self, button: IChipButton):
        pass

    @abstractmethod
    def add_chips(self, items: list[str]) -> None:
        pass

    @abstractmethod
    def remove_chips(self, items: list[str]) -> None:
        pass

    @abstractmethod
    def remove_all(self, *_) -> None:
        pass
