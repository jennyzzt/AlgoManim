
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl

from gui.custom_renderer import custom_renderer
from gui.video_player import VideoPlayerWidget
from gui.video_quality import VideoQuality
from gui.animation_bar import AnimationBar


WORKING_DIR = Path().absolute()

# Testing parameter
TEST_VIDEO_ONLY = False

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800


# ======== Main GUI ========


class GuiWindow(QDialog):

    # pylint: disable=too-many-instance-attributes
    # Instance attributes required to organise window.

    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_palette = QApplication.palette()

        self.setWindowTitle("AlgoManimHelper")

        # Python file path field
        pyfile_label = QLabel("Python File Relative Path:")
        self.pyfile_lineedit = QLineEdit()
        self.pyfile_lineedit.setPlaceholderText("Select a Python file")
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
        for (i, radio_button) in enumerate(radio_buttons):
            self.radio_btn_grp.addButton(radio_button, id=i)

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

        # Animation bar
        self.animation_bar = AnimationBar()

        # Video player
        self.video_player = VideoPlayerWidget(position_changed_callback=self.animation_bar.media_position_changed,
                                              parent=self)

        # Link animation bar and video player
        self.animation_bar.link_video_player(video_player=self.video_player)

        # Organise main window
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(text_layout, 0, 0, 1, -1)  # layout extends to right edge
        self.main_layout.addLayout(quality_layout, 1, 0, 1, -1)
        self.main_layout.addWidget(self.video_player, 2, 0, 1, -1)
        self.main_layout.addWidget(self.animation_bar, 3, 0, 1, -1)

        self.setLayout(self.main_layout)

    def show_file_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setDirectoryUrl(QUrl.fromLocalFile(str(WORKING_DIR)))

        file_path_str, _ = dialog.getOpenFileName(filter="Python files (*.py)")
        file_path = Path(file_path_str)

        if file_path.suffix == ".py":
            # Show chosen file's relative path in text box
            relpath = file_path.relative_to(WORKING_DIR)
            self.pyfile_lineedit.setText(str(relpath))

    def render_video(self):
        if TEST_VIDEO_ONLY:
            self.display_video(WORKING_DIR /
                               "media/algomanim/videos/BubbleSortScene.mp4")
            return

        # Retrieve render parameters
        pyfile_relpath = self.pyfile_lineedit.text()
        scene_name = self.scene_lineedit.text()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())

        # Render video programmatically
        anims = custom_renderer(pyfile_relpath, scene_name, video_quality)

        # Add animation boxes to scrollbar
        self.animation_bar.fill_bar(anims)

        # Display video
        video_fp = WORKING_DIR / f'media/algomanim/videos/{scene_name}.mp4'
        self.video_player.open_video(video_fp=video_fp)


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    gui.show()
    sys.exit(app.exec_())
