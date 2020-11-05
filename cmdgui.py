import ast
import os
import platform
import subprocess
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
from gui.panels.preconfig_panel import PreconfigPanel
from anim_change import AnimChange

WORKING_DIR = Path().absolute()
ERROR_MSG_STYLESHEET = "font: bold 13pt"

# Testing parameter
TEST_VIDEO_ONLY = False


# ======== Main GUI ========


class GuiWindow(QDialog):

    # pylint: disable=too-many-instance-attributes
    # Instance attributes required to organise window.
    # pylint: disable=too-many-statements
    # Statements necessary to piece widgets together.
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_palette = QApplication.palette()

        self.setWindowTitle("AlgoManim GUI")

        # ====================
        #     Video render
        # ====================

        # ========= File options =========

        # Python file path field
        pyfile_label = QLabel("Python File:")
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

        # ========= Quality options & action buttons =========

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
        self.render_button = QPushButton("Render")
        self.render_button.clicked.connect(self.render_video)

        # Show video in browser button
        self.show_video_button = QPushButton("Show video in explorer")
        self.show_video_button.clicked.connect(self.show_video_in_explorer)
        self.show_video_button.hide()  # hide until a video is rendered

        # These buttons should grow in height if more options are added later
        self.render_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.show_video_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Arrange radio buttons
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        for btn in radio_buttons:
            quality_layout.addWidget(btn)
        quality_layout.addStretch(1)
        quality_layout.addWidget(self.show_video_button)
        quality_layout.addWidget(self.render_button)

        # ========= Groupbox =========

        options_layout = QVBoxLayout()
        options_layout.addLayout(text_layout)
        options_layout.addLayout(quality_layout)

        options_groupbox = QGroupBox()
        options_groupbox.setLayout(options_layout)
        options_groupbox.setTitle("Render options")

        # =====================
        #     Animation bar
        # =====================

        self.animation_bar = AnimationBar()
        self.animation_bar.link_gui_window(self)

        # =====================
        #       Side menu
        # =====================

        # Keep track of animation changes to be applied
        self.changes = dict()

        # Panels for side menu
        self.customise_panel = CustomisePanel(changes=self.changes)
        self.customise_panel.link_gui_window(self)

        self.change_history_panel = ChangeHistoryPanel()
        self.change_history_panel.link_gui_window(self)

        self.preconfig_panel = PreconfigPanel()
        self.preconfig_panel.link_gui_window(self)

        # Initialize scene vars set by render
        self.scene_name = ""
        self.scene = None
        self.anims = None

        # Side menu toggle button
        self.menu_toggle = QToolButton()
        self.menu_toggle.setIcon(self.style()
                                 .standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton))
        self.menu_toggle.setFixedSize(25, 150)
        self.menu_toggle.clicked.connect(self.toggle_sidemenu)

        # Side menu
        self.tab_menu = QTabWidget(parent=self)
        self.tab_menu.addTab(self.customise_panel, "Customize")
        self.tab_menu.addTab(self.change_history_panel, "Change History")
        self.tab_menu.addTab(self.preconfig_panel, "Preconfig")
        self.tab_menu.hide()  # side menu hidden on gui initialisation

        # =====================
        #      Video player
        # =====================

        self.video_player = VideoPlayerWidget(position_changed_callback=
                                              self.animation_bar.media_position_changed,
                                              parent=self)
        self.animation_bar.link_video_player(video_player=self.video_player)

        # ==========================
        #     Main window layout
        # ==========================

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(options_groupbox, 0, 0)
        self.main_layout.addWidget(self.video_player, 1, 0)
        self.main_layout.addWidget(self.animation_bar, 2, 0)

        self.main_layout.addWidget(self.menu_toggle, 0, 1, -1, -1)
        self.main_layout.addWidget(self.tab_menu, 0, 2, -1, -1)

        # Set window to original size when side menu is closed
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)

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

    def show_video_in_explorer(self):
        path = self.video_player.video_fp
        if platform.system() == "Windows":
            subprocess.Popen(["explorer", "/select,", path])
        else:
            # MacOS or Linux
            subprocess.Popen(["open", "-R", path])

    def toggle_sidemenu(self):
        if self.tab_menu.isHidden():
            # display menu and reverse icon
            self.tab_menu.show()
            self.menu_toggle.setIcon(self.style()
                                     .standardIcon(QStyle.SP_MediaSeekBackward))
        else:
            # hide menu and reverse icon
            self.tab_menu.hide()
            self.menu_toggle.setIcon(self.style()
                                     .standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton))

    # opens side menu if it is not yet open
    def open_sidemenu(self):
        if self.tab_menu.isHidden():
            # display menu and reverse icon
            self.tab_menu.show()
            self.menu_toggle.setIcon(self.style()
                                     .standardIcon(QStyle.SP_MediaSeekBackward))

    def anim_clicked(self, anim):
        self.change_panel_anim(anim)
        # also opens the side menu if it is not yet open
        self.open_sidemenu()

    # just updates the customisation options in the panel
    def change_panel_anim(self, anim):
        self.customise_panel.set_animation(anim)

    def add_change(self, action_pair_index, change_name, change_type, change_value):
        change_key = (action_pair_index, change_type)
        anim_change = AnimChange(action_pair_index, change_name, change_type, change_value)
        # if animchange has already been added to dictionary of changes, update value
        # else add it to the dictionary
        if change_key not in self.changes:
            self.changes[change_key] = anim_change
            self.change_history_panel.add_change(anim_change)
        else:
            self.changes[change_key].update_value(change_value)
            self.change_history_panel.update_change(anim_change)

    def reset_changes(self):
        self.changes = dict()
        self.change_history_panel.reset()

    def apply_changes(self):
        curr_changes = self.changes.copy()
        def post_customize(action_pairs):
            for (action_pair_index, change_type), anim_change in curr_changes.items():
                change_type.customise(action_pairs[action_pair_index])(anim_change.get_value())
        self.scene.post_customize_fns.append(post_customize)
        self.render_video(rerender=True)
        # Do the rendering here
        self.reset_changes()

    def set_settings(self, label, value):
        # Catch cases that route to custom_renderer
        self.scene.post_config_settings[label] = value

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

    def render_video(self, rerender=False):
        if TEST_VIDEO_ONLY:
            self.video_player.open_video(WORKING_DIR /
                                         "media/algomanim/videos/BubbleSortScene.mp4")
            return

        if rerender:
            self.scene.rerender()
            self.anims = self.scene.metadata_blocks
        else:
            # Retrieve render parameters
            pyfile_relpath = self.pyfile_lineedit.text()
            self.scene_name = self.scene_combobox.currentText()
            background_color = self.scene.settings['background_color'] \
                if self.scene else None
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
            self.scene = custom_renderer(pyfile_relpath, self.scene_name,
                                        video_quality, background_color)
            self.anims = self.scene.metadata_blocks

        # Add animation boxes to scrollbar
        self.animation_bar.fill_bar(self.anims)

        # Add preconfig settings to panel
        self.preconfig_panel.load_settings(self.scene.settings)

        # Display video
        video_fp = WORKING_DIR / f'media/algomanim/videos/{self.scene_name}.mp4'
        self.video_player.open_video(video_fp=video_fp)

        # Display button
        self.show_video_button.show()


if __name__ == '__main__':
    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.show()
    sys.exit(app.exec_())
