
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from enum import Enum
from gui.video_player import VideoPlayerWidget
import sys
import subprocess

from pathlib import Path

WORKING_DIR = Path().absolute()

# Testing parameter
TEST_VIDEO = False


# ======== Helpers ========


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

    low = 0, "-l"
    med = 1, "-m"
    high = 2, "--high_quality"

    @staticmethod
    def retrieve_by_index(index):
        for quality in VideoQuality:
            if quality.index == index:
                return quality
        return None


# ======== Main GUI ========


class GuiWindow(QDialog):
    def __init__(self, parent=None):
        super(GuiWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("AlgoManimHelper")

        # Python file path field
        pyfile_label = QLabel("Python File Relative Path:")
        self.pyfile_lineedit = QLineEdit("")
        # Enforce file selection via dialog
        self.pyfile_lineedit.setReadOnly(True)
        pyfile_label.setBuddy(self.pyfile_lineedit)

        # File selection dialog
        pyfile_select_button = QPushButton()
        pyfile_select_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        pyfile_select_button.clicked.connect(self.show_file_dialog)

        # Scene name field
        scene_label = QLabel("Scene Name:")
        self.scene_lineedit = QLineEdit("")
        scene_label.setBuddy(self.scene_lineedit)

        # Arrange text fields
        text_layout = QHBoxLayout()
        text_layout.addWidget(pyfile_label)
        text_layout.addWidget(self.pyfile_lineedit, stretch=1)
        text_layout.addWidget(pyfile_select_button)
        text_layout.addWidget(scene_label)
        text_layout.addWidget(self.scene_lineedit, stretch=1)

        # Quality radio buttons
        quality_label = QLabel("Video Quality:")

        # Array order is tied to VideoQuality enum values
        radio_buttons = [QRadioButton("Low"),
                         QRadioButton("Medium"),
                         QRadioButton("High")]
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

        # Video player
        self.video_player = VideoPlayerWidget(video_fp=None, parent=self)

        # Organise main window
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(text_layout, 0, 0, 1, -1)  # layout extends to right edge
        self.main_layout.addLayout(quality_layout, 1, 0, 1, -1)
        self.main_layout.addWidget(self.video_player, 2, 0, 1, -1)

        self.setLayout(self.main_layout)

    def show_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setDirectoryUrl(QUrl.fromLocalFile(str(WORKING_DIR)))

        fp_str, _ = dialog.getOpenFileName(filter="Python files (*.py)")
        fp = Path(fp_str)

        if fp.suffix == ".py":
            # Show chosen file's relative path in text box
            relpath = fp.relative_to(WORKING_DIR)
            self.pyfile_lineedit.setText(str(relpath))

    def render_video(self):
        if TEST_VIDEO:
            self.show_video_on_render_success(WORKING_DIR / "media/videos/bubblesort/480p15/BubbleSortScene.mp4")
            return

        pyfile_relpath = self.pyfile_lineedit.text()
        scene_name = self.scene_lineedit.text()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())

        # Render video
        process = subprocess.Popen(['python3', '-m', 'manim',
                                    pyfile_relpath, scene_name, video_quality.cmdflag],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        # TODO: show progress
        stdout, stderr = process.communicate()

        # Retrieves file not found error
        # scene-not-in-script error would be at index 1
        errmsg = stderr.decode("utf-8").splitlines()[-1]

        if errmsg.isspace():
            # success
            video_fp = self.get_video_fp_from_stdout(stdout=stdout.decode("utf-8"))
            self.show_video_on_render_success(video_fp)
        else:
            # failed to output video
            # TODO: handle fnf and scene-not-in-script errors visibly
            print(errmsg)

    @staticmethod
    def get_video_fp_from_stdout(stdout):
        fp = ""
        # target line format is "File ready at <video_path>"
        for line in stdout.splitlines():
            if line.startswith("File ready at"):
                fp = line.split()[-1]
        return fp

    def show_video_on_render_success(self, video_fp):
        # Set video filepath in the player
        self.video_player.video_fp = video_fp

        # Open the video
        self.video_player.open_video()


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.show()
    sys.exit(app.exec_())
