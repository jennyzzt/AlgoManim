from PyQt5.QtWidgets import *

# Scrollbar minimum width
SCROLL_WIDTH = 300


class BaseChangesPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up scrollbar
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumWidth(SCROLL_WIDTH)

        # Buttons
        save_button = QPushButton("Save changes")
        apply_button = QPushButton("Apply changes and render")

        # Arrange widget contents
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(save_button)
        self.main_layout.addWidget(apply_button)

        self.setLayout(self.main_layout)
