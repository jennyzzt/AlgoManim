import ast
import os
import platform
import subprocess
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, pyqtSlot

from algomanim.empty_animation import empty_animation
from gui.custom_renderer import custom_renderer
from gui.progress_bar import RenderProgressBar, VideoRenderThread
from gui.video_player import VideoPlayerWidget
from gui.video_quality import VideoQuality
from gui.animation_bar import AnimationBar, is_empty_anim
from gui.panels.customise_panel import CustomisePanel
from gui.panels.change_history_panel import ChangeHistoryPanel
from gui.panels.preconfig_panel import PreconfigPanel
from anim_change import AnimChange


WORKING_DIR = Path().absolute()
ERROR_MSG_STYLESHEET = "font: bold 13pt"

# controls whether shortcut button to load toyexample.py is shown
DEBUG = False


# ======== Main GUI ========


class GuiWindow(QMainWindow):

    # pylint: disable=too-many-instance-attributes
    # Instance attributes required to organise window.
    # pylint: disable=too-many-statements
    # Statements necessary to piece widgets together.
    # pylint: disable=too-many-locals
    # Variables required to piece together UI

    # pylint: disable=too-many-public-methods

    def __init__(self, parent=None):
        super().__init__(parent)

        # QMainWindow boilerplate
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.original_palette = QApplication.palette()

        self.setWindowTitle("AlgoManim GUI")

        # ====================
        #     Video render
        # ====================

        self.worker = None

        # ========= File options =========

        # Python file path field
        pyfile_label = QLabel("Python File:")
        self.pyfile_lineedit = QLineEdit()
        self.pyfile_lineedit.setPlaceholderText("Select a Python file")

        # The previous file rendered
        self.prev_pyfile = ""

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

        if DEBUG:
            self.debug_button = QPushButton("ToyExample")
            self.debug_button.clicked.connect(self.render_toyexample)

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
        if DEBUG:
            quality_layout.addWidget(self.debug_button)
        quality_layout.addWidget(self.render_button)

        # ========= Busy indicator / Progress bar =========

        self.render_progress_bar = RenderProgressBar()

        # ========= Groupbox =========

        options_layout = QVBoxLayout()
        options_layout.addLayout(text_layout)
        options_layout.addLayout(quality_layout)
        options_layout.addWidget(self.render_progress_bar)
        self.render_progress_bar.hide()

        options_groupbox = QGroupBox()
        options_groupbox.setLayout(options_layout)
        options_groupbox.setTitle("Render options")

        # ===========================================
        #     Animation bar and MultiBlock Edits
        # ===========================================

        self.mb_start_idx = None
        self.mb_end_idx = None
        self.choose_mb_start = False
        self.choose_mb_end = False

        self.mb_layout = QVBoxLayout()

        mb_edit_layout = QHBoxLayout()
        mb_edit_label = QLabel("Choose Multiple Blocks: ")
        self.mb_start_btn = QPushButton("Select Start Block")
        self.mb_end_btn = QPushButton("Select End Block")
        self.mb_start_btn.clicked.connect(self.toggle_mb_start)
        self.mb_end_btn.clicked.connect(self.toggle_mb_end)
        mb_edit_layout.addWidget(mb_edit_label)
        mb_edit_layout.addWidget(self.mb_start_btn)
        mb_edit_layout.addWidget(self.mb_end_btn)

        self.animation_bar = AnimationBar()
        self.animation_bar.link_gui_window(self)

        self.mb_layout.addLayout(mb_edit_layout)
        self.mb_layout.addWidget(self.animation_bar)

        # =====================
        #       Side menu
        # =====================

        # Keep track of animation changes to be applied
        self.changes = dict()
        self.insertions = dict()
        self.post_customize_fns = []
        self.post_config_settings = dict()

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
        self.main_layout.addLayout(self.mb_layout, 2, 0)

        self.main_layout.addWidget(self.menu_toggle, 0, 1, -1, -1)
        self.main_layout.addWidget(self.tab_menu, 0, 2, -1, -1)

        # Set window to original size when side menu is closed
        self.main_layout.setSizeConstraint(QLayout.SetFixedSize)

        self.central_widget.setLayout(self.main_layout)

    def toggle_mb_start(self):
        self.choose_mb_start = not self.choose_mb_start
        self.mb_start_btn.setDown(self.choose_mb_start)
        self.animation_bar.set_multiblock_selection_mode(self.choose_mb_start)

    def toggle_mb_end(self):
        self.choose_mb_end = not self.choose_mb_end
        self.mb_end_btn.setDown(self.choose_mb_end)
        self.animation_bar.set_multiblock_selection_mode(self.choose_mb_end)

    @staticmethod
    def show_error(error_msg, info_text=None):
        err = QMessageBox(icon=QMessageBox.Critical,
                            text=error_msg)
        err.setInformativeText(info_text)
        err.setStandardButtons(QMessageBox.Close)
        err.setStyleSheet(ERROR_MSG_STYLESHEET)
        err.exec_()

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
        system_type = platform.system()
        if system_type == "Windows":
            subprocess.Popen(["explorer", "/select,", path])
        elif system_type == "Linux":
            subprocess.Popen(["xdg-open", path.parent])
        elif system_type == "Darwin":
            subprocess.Popen(["open", "-R", path])
        else:
            print(f'Feature not supported in platform: {system_type}')

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
        # opens the side menu if it is not yet open
        self.open_sidemenu()

        if self.choose_mb_start:
            self.mb_start_idx = self.anims.index(anim)
            self.toggle_mb_start()

        if self.choose_mb_end:
            self.mb_end_idx = self.anims.index(anim)
            self.toggle_mb_end()

            self.multiblock_select(self.mb_start_idx, self.mb_end_idx)
            return True

        self.change_panel_anim(anim)
        return False

    # just updates the customisation options in the panel
    def change_panel_anim(self, anim):
        self.customise_panel.set_animation(anim)

    # add a customisation change
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

    def insert_animations(self, insertions):
        self.insertions.update(insertions)
        self.change_history_panel.add_insertions(insertions)

    def reset_changes(self):
        self.changes = dict()
        self.insertions = dict()
        self.post_customize_fns = []
        self.post_config_settings = dict()
        self.change_history_panel.reset()

    def apply_changes(self):
        curr_changes = self.changes.copy()
        def customize_anims(algoscene):
            action_pairs = algoscene.action_pairs
            for (action_pair_index, change_type), anim_change in curr_changes.items():
                change_type.customise(action_pairs[action_pair_index])(anim_change.get_value())
        self.post_customize_fns.append(customize_anims)

        def insert_anims(algoscene):
            insertions = sorted(list(self.insertions.items()), reverse=True)
            for index, insertion in insertions:
                if text := insertion.get('slide'):
                    algoscene.add_slide(text, index)
                if wait_time_str := insertion.get('wait'):
                    try:
                        wait_time = float(wait_time_str)
                        algoscene.add_wait(index, wait_time=wait_time)
                    except ValueError:
                        self.show_error(f"{wait_time_str} is an invalid float",
                        info_text=f"Skipped insertion of wait at {index}")
        self.post_customize_fns.append(insert_anims)

        self.render_video(keep_changes=True)

    def set_settings(self, label, value):
        # Catch cases that route to custom_renderer
        self.post_config_settings[label] = value

    def add_empty_anim(self, index, position):
        self.anims.insert(index, empty_animation(position))
        self.animation_bar.fill_bar(self.anims)

    def delete_empty_anim(self, index):
        self.anims.pop(index)
        self.animation_bar.fill_bar(self.anims)

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

    def render_toyexample(self):
        self.scene_name = "ToyScene"

        # Render video programmatically
        self.scene = custom_renderer("algomanim_examples/toyexample.py",
                                     self.scene_name, VideoQuality.low,
                                     self.post_customize_fns, self.post_config_settings)
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

    def render_video(self, keep_changes=False):
        # Retrieve render parameters
        pyfile_relpath = self.pyfile_lineedit.text()
        self.scene_name = self.scene_combobox.currentText()
        video_quality = VideoQuality.retrieve_by_index(self.radio_btn_grp.checkedId())

        # Check that the python file exists
        if not os.path.exists(pyfile_relpath):
            self.show_error("File does not exist",
                info_text="The python file no longer exists at the given location."
                          "Select another file to proceed.")
            return

        # Check that a scene has been selected
        if self.scene_combobox.currentIndex() < 0:
            self.show_error("No scene selected",
                info_text="You must select a scene to render")
            return

        if (self.prev_pyfile and self.prev_pyfile != pyfile_relpath)\
                or not keep_changes:
            # prev_pyfile is not empty and a different file is being rendered
            # or the scene changed
            # Clear previous settings
            self.reset_changes()

        # Update prev_pyfile
        self.prev_pyfile = pyfile_relpath

        # Render video programmatically
        # Create worker thread
        self.worker = VideoRenderThread(pyfile_relpath, self.scene_name,
                                        video_quality, self.post_customize_fns,
                                        self.post_config_settings)
        self.worker.exceptioned.connect(self.render_failed)
        self.worker.task_finished.connect(lambda scene: self.render_finished(scene))

        # Set progress bar to busy
        self.on_render_start()

        # Start worker
        self.worker.start()

    def on_render_start(self):
        self.render_progress_bar.show()
        self.render_progress_bar.set_busy()

    def on_render_finish(self):
        # Set to unbusy
        self.render_progress_bar.set_idle()
        self.render_progress_bar.hide()

    @pyqtSlot(Exception)
    def render_failed(self, exception):
        # Print error message to console
        print(exception)

        # Display error message on GUI
        info_str = f"The input file could not be rendered." \
                   f"\n\nError: {exception}"
        self.show_error("Input file error", info_text=info_str)

        # Stop the progress bar
        self.on_render_finish()

    @pyqtSlot(object)
    def render_finished(self, scene):
        self.on_render_finish()

        # Update the GUI
        self.scene = scene
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


    def multiblock_select(self, start, end):
        # swap start and end if they have been selected the other way around
        if start > end:
            start, end = end, start

        contains_empty_anim = any([is_empty_anim(anim) for anim in self.anims[start:end + 1]])
        if contains_empty_anim:
            err = QMessageBox(icon=QMessageBox.Critical,
                              text="Please render first")
            err.setInformativeText('You have added a text slide. Please click on \
                \'Apply Changes and Render\' before continuing')
            err.setStandardButtons(QMessageBox.Close)
            err.setStyleSheet(ERROR_MSG_STYLESHEET)
            err.exec_()
            return

        self.animation_bar.set_animation_group(self.anims[start], self.anims[end])
        self.customise_panel.set_animation_group(self.anims[start:end + 1])


if __name__ == '__main__':
    # set global debug flag
    # pylint: disable=simplifiable-if-statement
    if len(sys.argv) > 1 and sys.argv[1] == "-debug":
        DEBUG = True
    else:
        DEBUG = False

    app = QApplication([])  # no cmd line params
    gui = GuiWindow()
    gui.show()
    sys.exit(app.exec_())
