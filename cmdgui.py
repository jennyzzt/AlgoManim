import ast
import os
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl

from gui.custom_renderer import custom_renderer
from gui.video_player import VideoPlayerWidget
from gui.video_quality import VideoQuality
from gui.animation_bar import AnimationBar
from gui.panels.customise_panel import CustomisePanel
from gui.panels.change_history_panel import ChangeHistoryPanel
from anim_change import AnimChange

WORKING_DIR = Path().absolute()
ERROR_MSG_STYLESHEET = "font: bold 13pt"

# Testing parameter
TEST_VIDEO_ONLY = False


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
        self.scene_combobox = QComboBox()
        self.scene_combobox.setPlaceholderText("Select a scene")
        scene_label.setBuddy(self.scene_combobox)

        # Arrange text fields
        text_layout = QHBoxLayout()
        text_layout.addWidget(pyfile_label)
        text_layout.addWidget(self.pyfile_lineedit, stretch=1)
        text_layout.addWidget(pyfile_select_button)
        text_layout.addWidget(scene_label)
        text_layout.addWidget(self.scene_combobox, stretch=1)

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

        # Panels for side menu
        self.customise_panel = CustomisePanel()
        # self.animation_bar.link_changes_panel(self.customise_panel)

        self.change_history_panel = ChangeHistoryPanel()
        self.animation_bar.link_changes_panel(self.change_history_panel)
        # Keep track of animation changes to be applied
        self.changes = []

        # Side menu
        self.tab_menu = QTabWidget(parent=self)
        self.tab_menu.addTab(self.customise_panel, "Customize")
        self.tab_menu.addTab(self.change_history_panel, "Change History")

        # Video player
        self.video_player = VideoPlayerWidget(position_changed_callback=
                                              self.animation_bar.media_position_changed,
                                              parent=self)
        self.animation_bar.link_video_player(video_player=self.video_player)

        # Organise main window
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(text_layout, 0, 0)
        self.main_layout.addLayout(quality_layout, 1, 0)
        self.main_layout.addWidget(self.video_player, 2, 0)
        self.main_layout.addWidget(self.animation_bar, 3, 0)

        self.main_layout.addWidget(self.tab_menu, 0, 1, -1, -1)

        self.setLayout(self.main_layout)

    def show_file_dialog(self):
        dialog = QFileDialog()
        dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setDirectoryUrl(QUrl.fromLocalFile(str(WORKING_DIR)))

        file_path_str, _ = dialog.getOpenFileName(filter="Python files (*.py)")
        file_path = Path(file_path_str)

        if file_path.suffix == ".py":
            # Show chosen file's relative path in text box
            relpath = file_path.relative_to(WORKING_DIR)
            self.pyfile_lineedit.setText(str(relpath))

            # Clear any previous entries and (re)fill combobox
            self.scene_combobox.clear()
            for name in self.get_scene_names(file_path_str):
                self.scene_combobox.addItem(name)

    def add_change(self, anim, change_type, input_widget):
        anim_change = AnimChange(anim, change_type, input_widget)
        self.changes.append(anim_change)
        self.change_history_panel.add_change(anim_change)

    def reset_changes(self):
        self.changes = []
        self.change_history_panel.reset()

    def apply_changes(self):
        for change in self.changes:
            change.apply()
        # Do the rendering here
        self.reset_changes()

    # Returns list of AlgoScene subclasses in the Python file at python_fp
    @staticmethod
    def get_scene_names(python_fp):
        with open(python_fp) as file:
            node = ast.parse(file.read())

        scene_names = []
        all_classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        for cls in all_classes:
            if "AlgoScene" in [base.id for base in cls.bases]:
                scene_names.append(cls.name)

        return scene_names

    def render_video(self):
        if TEST_VIDEO_ONLY:
            self.video_player.open_video(WORKING_DIR /
                                         "media/algomanim/videos/BubbleSortScene.mp4")
            return

        # Retrieve render parameters
        pyfile_relpath = self.pyfile_lineedit.text()
        scene_name = self.scene_combobox.currentText()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())

        # Check that the python file exists
        if not os.path.exists(pyfile_relpath):
            err = QMessageBox(icon=QMessageBox.Critical,
                              text="File does not exist")
            err.setInformativeText('The python file no longer exists at the given location. '
                                   'Select another file to proceed.')
            err.setStandardButtons(QMessageBox.Close)
            err.setStyleSheet(ERROR_MSG_STYLESHEET)
            err.exec_()
            return

        # Check that a scene has been selected
        if self.scene_combobox.currentIndex() < 0:
            err = QMessageBox(icon=QMessageBox.Critical,
                              text="No scene selected")
            err.setInformativeText('You must select a scene to render')
            err.setStandardButtons(QMessageBox.Close)
            err.setStyleSheet(ERROR_MSG_STYLESHEET)
            err.exec_()
            return

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
    gui.show()
    sys.exit(app.exec_())
