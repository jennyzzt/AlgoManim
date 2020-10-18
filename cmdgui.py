
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
import sys


class GuiWindow(QDialog):
    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("AlgoManimHelper")

        # Python file path field
        pyfile_lineedit = QLineEdit("")
        pyfile_label = QLabel("&Python File:")
        pyfile_label.setBuddy(pyfile_lineedit)

        # Scene name field
        scene_lineedit = QLineEdit("")
        scene_label = QLabel("&Scene Name:")
        scene_label.setBuddy(scene_lineedit)

        # Arrange text fields
        top_layout = QHBoxLayout()
        top_layout.addWidget(pyfile_label)
        top_layout.addWidget(pyfile_lineedit, stretch=1)
        top_layout.addWidget(scene_label)
        top_layout.addWidget(scene_lineedit, stretch=1)

        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, -1)  # layout extends to right edge

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.resize(640, 480)
    gui.show()
    sys.exit(app.exec_())
