from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.video_player import VIDEO_BASE_WIDTH


# Scrollbar base height
BAR_BASE_HEIGHT = 150


class AnimationBar(QWidget):

    def __init__(self, video_player=None, gui_window=None, parent=None):
        super().__init__(parent)

        self.video_player = video_player
        self.gui_window = gui_window

        self.anims = []
        self.anim_boxes = []
        self.anim_box_list = QHBoxLayout()
        self.anim_box_list.setContentsMargins(0, 0, 0, 0)

        # Set up scrollbar for boxes
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumSize(VIDEO_BASE_WIDTH, BAR_BASE_HEIGHT)

        # Arrange widget contents
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

    def link_video_player(self, video_player):
        self.video_player = video_player

    def link_gui_window(self, gui_window):
        self.gui_window = gui_window

    def fill_bar(self, anims):
        self.anims = anims
        self.anim_boxes = []
        self.anim_box_list = QHBoxLayout()
        self.anim_box_list.setContentsMargins(0, 0, 0, 0)

        for anim in self.anims:
            anim_box = self.create_anim_box(anim)
            self.anim_box_list.addWidget(anim_box)
            self.anim_boxes.append(anim_box)

        # Group boxes together
        anim_group_box = QGroupBox()
        anim_group_box.setStyleSheet("border-style: none")
        anim_group_box.setLayout(self.anim_box_list)

        # Show boxes in scroll area
        self.scroll_area.setWidget(anim_group_box)

    def create_anim_box(self, anim):
        """
        Create a single anim box from the properties of anim
        """
        # Get all relevant animation information stored in the action pair metadata
        # anim_infos = dict.fromkeys(map(lambda action: action.metadata, anim['action_pairs']))
        # anim_info = [f'{info.metadata.name}' for info in anim_infos if info is not None]
        # if anim_info:
        #    desc = '\n'.join(anim_info)
        # else:
        #    # Lacks metadata, assume custom animation
        #    desc = 'Custom Animation'
        desc = 'Custom Animation'

        anim_box = QGroupBox()
        anim_box.setStyleSheet("border-style: none; background-color: white; color: black")

        anim_box_layout = QVBoxLayout()
        anim_box_layout.setContentsMargins(0, 0, 0, 0)

        anim_lbl = QLabel(desc)
        anim_lbl.setAlignment(Qt.AlignCenter)
        anim_lbl.setWordWrap(True)

        # Size box
        anim_box.setFixedHeight(BAR_BASE_HEIGHT - 20)  # prevent height overflow
        width = max(int(150 * anim.runtime_val()), 80)
        anim_box.setFixedWidth(width)

        # Layout anim box
        anim_box_layout.addWidget(anim_lbl)
        anim_box.setLayout(anim_box_layout)

        # Clicking on anim box jumps video to anim
        anim_box.mouseReleaseEvent = lambda event: \
            self.set_mouse_clicked(anim)

        return anim_box

    def set_mouse_clicked(self, anim):
        self.video_player.set_media_position(anim.start_position())
        self.gui_window.anim_clicked(anim)

    def set_active_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: #2980b9; color: white")
        self.scroll_area.ensureWidgetVisible(self.anim_boxes[index])

    def set_inactive_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: white; color: black")

    def media_position_changed(self, position):
        for (i, anim) in enumerate(self.anims):
            start_position = anim.start_position()
            end_position = anim.end_position()
            if (start_position <= position < end_position) or \
                (start_position == position and start_position == end_position):
                self.set_active_lbl(i)
                self.gui_window.anim_clicked(anim)
            else:
                self.set_inactive_lbl(i)
