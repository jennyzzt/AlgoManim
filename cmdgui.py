
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt

from custom_renderer import custom_renderer
from gui.video_player import VideoPlayerWidget
from gui.video_quality import VideoQuality


WORKING_DIR = Path().absolute()

# Testing parameter
TEST_VIDEO = False

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

        # Video player
        self.video_player = VideoPlayerWidget(video_fp=None,
                                              position_changed_callback=self.media_position_changed,
                                              parent=self)

        # Animation Scrubber
        self.anim_scrubber = None
        self.anim_boxes = []
        self.anims = []

        # Organise main window
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(text_layout, 0, 0, 1, -1)  # layout extends to right edge
        self.main_layout.addLayout(quality_layout, 1, 0, 1, -1)
        self.main_layout.addWidget(self.video_player, 2, 0, 1, -1)

        self.setLayout(self.main_layout)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

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
        if TEST_VIDEO:
            self.show_video_on_render_success(WORKING_DIR /
                                              "media/videos/bubblesort/480p15/BubbleSortScene.mp4")
            return

        pyfile_relpath = self.pyfile_lineedit.text()
        scene_name = self.scene_lineedit.text()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())

        # Render Video Programmatically
        self.anims = custom_renderer(pyfile_relpath, scene_name, video_quality)
        video_fp = WORKING_DIR / f'./media/algomanim/videos/{scene_name}.mp4'
        self.create_anims_scrubber()
        self.show_video_on_render_success(video_fp)

    def create_anims_scrubber(self):
        """
        Create horizontal list of anim boxes as an animation scrubber
        """
        # Animation Scrubber
        anim_box_list = QHBoxLayout()
        anim_box_list.setContentsMargins(0, 0, 0, 0)
        self.anim_boxes = []
        for anim in self.anims:
            anim_box = self.create_anim_box(anim)
            anim_box_list.addWidget(anim_box)
            self.anim_boxes.append(anim_box)
        anim_group_box = QGroupBox()
        anim_group_box.setStyleSheet("border-style: none")
        anim_group_box.setLayout(anim_box_list)

        # remove previous anim_scrubber if it already exists
        if self.anim_scrubber is not None:
            self.main_layout.removeWidget(self.anim_scrubber)
        self.anim_scrubber = QScrollArea()
        self.anim_scrubber.setWidget(anim_group_box)
        self.anim_scrubber.setFixedHeight(100)
        self.main_layout.addWidget(self.anim_scrubber, 3, 0, 1, -1)

    def create_anim_box(self, anim):
        """
        Create a single anim box from the properties of anim
        """
        desc = f'Animation\n{anim["start_index"] + 1}' if anim['start_index'] == anim['end_index'] \
            else f'Animation\n{anim["start_index"] + 1} - {anim["end_index"] + 1}'
        anim_box = QGroupBox()
        anim_box.setStyleSheet("border-style: none; background-color: white; color: black")
        anim_box_layout = QVBoxLayout()
        anim_box_layout.setContentsMargins(0, 0, 0, 0)
        anim_lbl = QLabel(desc)
        anim_lbl.setAlignment(Qt.AlignCenter)
        anim_lbl.setWordWrap(True)
        anim_box.setFixedHeight(100)
        width = max(int(150 * anim['run_time']), 80)
        anim_box.setFixedWidth(width)

        btn_layout = QHBoxLayout()
        runtime_btn = QPushButton()
        runtime_btn_policy = runtime_btn.sizePolicy()
        runtime_btn_policy.setRetainSizeWhenHidden(True)
        runtime_btn.setSizePolicy(runtime_btn_policy)
        runtime_btn.setFixedHeight(40)
        runtime_btn.setFixedWidth(40)
        runtime_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        color_btn = QPushButton()
        color_btn_policy = color_btn.sizePolicy()
        color_btn_policy.setRetainSizeWhenHidden(True)
        color_btn.setSizePolicy(color_btn_policy)
        color_btn.setFixedHeight(40)
        color_btn.setFixedWidth(40)
        color_btn.setIcon(self.style().standardIcon(QStyle.SP_DriveCDIcon))

        if not anim['can_change_runtime']:
            runtime_btn.hide()
        if not anim['can_change_color']:
            color_btn.hide()
        btn_layout.addWidget(runtime_btn)
        btn_layout.addWidget(color_btn)

        anim_box_layout.addLayout(btn_layout)
        anim_box_layout.addWidget(anim_lbl)
        anim_box.setLayout(anim_box_layout)

        anim_box.mouseReleaseEvent = lambda event: \
            self.video_player.set_media_position(anim['start_time'] * 1000)
        return anim_box

    def set_active_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: #2980b9; color: white")
        self.anim_scrubber.ensureWidgetVisible(self.anim_boxes[index])

    def set_inactive_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: white; color: black")

    def media_position_changed(self, position):
        for (i, anim) in enumerate(self.anims):
            start_time = anim['start_time'] * 1000
            end_time = (anim['start_time'] + anim['run_time']) * 1000
            if start_time <= position <= end_time:
                self.set_active_lbl(i)
            else:
                self.set_inactive_lbl(i)

    @staticmethod
    def get_video_fp_from_stdout(stdout):
        # target line format is "File ready at <video_path>"
        for line in stdout.splitlines():
            if line.startswith("File ready at"):
                return line.split()[-1]
        return ""

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
