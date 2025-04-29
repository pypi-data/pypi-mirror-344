from PyQt6.QtWidgets import QListWidgetItem

from jb_qt.common import consts


def get_item_value(item: QListWidgetItem) -> str:
    value = item.data(consts.LIST_ITEM_ROLE) or item.text()
    return value.strip()
