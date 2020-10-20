
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from enum import Enum
import sys

# Initial window size hint values
WIDTH = 650
HEIGHT = 130


# Value tied to index in radio_buttons
class VideoQuality(Enum):

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, index, cmdflag):
        self.index = index
        self.cmdflag = cmdflag

    low = 0, "-ql"
    med = 1, "-qm"
    high = 2, "-qh"
    prod = 3, "-qp"
    four_k = 4, "-qk"

    @staticmethod
    def retrieve_by_index(index):
        for quality in VideoQuality:
            if quality.index == index:
                return quality
        return None


class GuiWindow(QDialog):
    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("AlgoManimHelper")

        # Python file path field
        pyfile_label = QLabel("Python File Relative Path:")
        self.pyfile_lineedit = QLineEdit("")
        pyfile_label.setBuddy(self.pyfile_lineedit)

        # Scene name field
        scene_label = QLabel("Scene Name:")
        self.scene_lineedit = QLineEdit("")
        scene_label.setBuddy(self.scene_lineedit)

        # Arrange text fields
        text_layout = QHBoxLayout()
        text_layout.addWidget(pyfile_label)
        text_layout.addWidget(self.pyfile_lineedit, stretch=1)
        text_layout.addWidget(scene_label)
        text_layout.addWidget(self.scene_lineedit, stretch=1)

        # Quality radio buttons
        quality_label = QLabel("Video Quality:")

        # Array order is tied to VideoQuality enum values
        radio_buttons = [QRadioButton("Low"),
                         QRadioButton("Medium"),
                         QRadioButton("High"),
                         QRadioButton("Production"),
                         QRadioButton("4K")]
        # Set default quality to Low
        radio_buttons[VideoQuality.low.value].setChecked(True)

        # Create button group for easy access
        self.radio_btn_grp = QButtonGroup()
        for i in range(len(radio_buttons)):
            self.radio_btn_grp.addButton(radio_buttons[i], id=i)

        # Render button
        render_button = QPushButton("Render")
        render_button.clicked.connect(self.render_video)

        # Arrange radio buttons
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        for btn in radio_buttons:
            quality_layout.addWidget(btn)
        quality_layout.addStretch(1)
        quality_layout.addWidget(render_button)

        # Organise main window
        main_layout = QGridLayout()
        main_layout.addLayout(text_layout, 0, 0, 1, -1)  # layout extends to right edge
        main_layout.addLayout(quality_layout, 1, 0, 1, -1)

        self.setLayout(main_layout)

    @pyqtSlot()
    def render_video(self):
        pyfile_relpath = self.pyfile_lineedit.text()
        scene_name = self.scene_lineedit.text()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.resize(WIDTH, HEIGHT)  # window size hint
    gui.show()
    sys.exit(app.exec_())
