from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog


class JbFileDialog(QWidget):
    selectedFile = pyqtSignal(str)

    def __init__(self, title: str = "File Dialog", directory: str = "") -> None:
        """Initialize the main window with a button to open a file dialog."""
        super().__init__()
        self.setWindowTitle("QFileDialog Example")
        self.directory = directory

        self.button = QPushButton("Open File", self)
        self.button.clicked.connect(self.open_file_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def open_file_dialog(self) -> None:
        """Open a file dialog to select a file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", self.directory, "All Files (*);;Text Files (*.txt)"
        )
        if file_name:
            self.selectedFile.emit(file_name)
