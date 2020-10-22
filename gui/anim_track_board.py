from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class AnimTrackBoard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.changes = []

        # Set up scrollbar for boxes
        self.scroll_area = QScrollArea()

        # Arrange widget contents
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)
