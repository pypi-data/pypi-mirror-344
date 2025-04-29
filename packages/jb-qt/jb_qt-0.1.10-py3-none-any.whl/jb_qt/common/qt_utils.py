from PyQt6.QtWidgets import QListWidgetItem, QApplication

from jb_qt.common import consts


def get_item_value(item: QListWidgetItem) -> str:
    value = item.data(consts.LIST_ITEM_ROLE) or item.text()
    return value.strip()


def register_app(app: QApplication, icon_dir: str = "") -> None:
    consts.GlobalRefs.app = app
    consts.set_icon_dir(icon_dir)
