
from PyQt5.QtWidgets import *
import sys

# Initial window size hint values
WIDTH = 650
HEIGHT = 130


class GuiWindow(QDialog):
    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("AlgoManimHelper")

        # Python file path field
        pyfile_lineedit = QLineEdit("")
        pyfile_label = QLabel("Python File Relative Path:")
        pyfile_label.setBuddy(pyfile_lineedit)

        # Scene name field
        scene_lineedit = QLineEdit("")
        scene_label = QLabel("Scene Name:")
        scene_label.setBuddy(scene_lineedit)

        # Arrange text fields
        text_layout = QHBoxLayout()
        text_layout.addWidget(pyfile_label)
        text_layout.addWidget(pyfile_lineedit, stretch=1)
        text_layout.addWidget(scene_label)
        text_layout.addWidget(scene_lineedit, stretch=1)

        # Quality radio buttons
        quality_label = QLabel("Video Quality:")
        radio_low = QRadioButton("Low")
        radio_med = QRadioButton("Medium")
        radio_high = QRadioButton("High")
        radio_prod = QRadioButton("Production")
        radio_4k = QRadioButton("4K")
        radio_low.setChecked(True)

        # Render button
        render_button = QPushButton("Render")
        render_button.setDefault(True)  # Can be triggered with Enter key (?)

        # Arrange radio buttons
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(radio_low)
        quality_layout.addWidget(radio_med)
        quality_layout.addWidget(radio_high)
        quality_layout.addWidget(radio_prod)
        quality_layout.addWidget(radio_4k)
        quality_layout.addStretch(1)
        quality_layout.addWidget(render_button)

        # Organise main window
        main_layout = QGridLayout()
        main_layout.addLayout(text_layout, 0, 0, 1, -1)  # layout extends to right edge
        main_layout.addLayout(quality_layout, 1, 0, 1, -1)

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.resize(WIDTH, HEIGHT)  # window size hint
    gui.show()
    sys.exit(app.exec_())
