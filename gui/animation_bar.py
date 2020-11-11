from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.video_player import VIDEO_BASE_WIDTH


# Scrollbar base height
BAR_BASE_HEIGHT = 125

# Box width constraints
BOX_MIN_WIDTH = 80
BOX_MAX_WIDTH = 320

def empty_animation(index):
    return {
        'index': index,
        'desc': "Add custom animations",
        'runtime': 0.5
    }

def is_empty_anim(anim):
    return not hasattr(anim, 'start_position')

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

        for index, anim in enumerate(self.anims):
            anim_box = self.create_anim_box(index, anim)
            self.anim_box_list.addWidget(anim_box)
            self.anim_boxes.append(anim_box)

        # Group boxes together
        anim_group_box = QGroupBox()
        anim_group_box.setStyleSheet("border-style: none")
        anim_group_box.setLayout(self.anim_box_list)

        # Show boxes in scroll area
        self.scroll_area.setWidget(anim_group_box)

    @staticmethod
    def get_anim_box_size(runtime):
        height = BAR_BASE_HEIGHT - 15  # prevent height overflow

        width = max(int(150 * runtime), BOX_MIN_WIDTH)
        width = min(width, BOX_MAX_WIDTH)  # prevent box from getting too long

        return width, height

    def create_anim_box(self, index, anim):
        """
        Create a single anim box from the properties of anim
        """
        desc = anim['desc'] if is_empty_anim(anim) else anim.desc()

        anim_box = QGroupBox()
        anim_box.setStyleSheet("border-style: none; background-color: white; color: black")

        anim_box_layout = QVBoxLayout()
        anim_box_layout.setContentsMargins(0, 0, 0, 0)

        # Create text animation button
        if not is_empty_anim(anim):
            add_anim_button = QPushButton(text='+')
            add_anim_button.setStyleSheet("border:1px solid black;")
            add_anim_button.clicked.connect(lambda event: self.add_anim(index + 1))
            anim_box_layout.addWidget(add_anim_button, alignment=Qt.AlignRight)

        # Animation label using metadata
        anim_lbl = QLabel(desc)
        anim_lbl.setAlignment(Qt.AlignCenter)
        anim_lbl.setWordWrap(True)
        anim_box_layout.addWidget(anim_lbl)

        # Size and layout box
        width, height = AnimationBar.get_anim_box_size(anim.runtime \
            if not is_empty_anim(anim) else anim['runtime'])
        anim_box.setFixedHeight(height)
        anim_box.setFixedWidth(width)
        anim_box.setLayout(anim_box_layout)

        # Clicking on anim box jumps video to anim
        anim_box.mouseReleaseEvent = lambda event: \
            self.set_mouse_clicked(anim)

        return anim_box

    def set_mouse_clicked(self, anim):
        if not is_empty_anim(anim):
            self.video_player.set_media_position(anim.start_position())
        self.gui_window.anim_clicked(anim)

    def set_active_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: #2980b9; color: white")
        self.scroll_area.ensureWidgetVisible(self.anim_boxes[index])

    def set_inactive_lbl(self, index):
        self.anim_boxes[index].setStyleSheet("background-color: white; color: black")

    def media_position_changed(self, position):
        # print(f'Media position changed to {position}')
        for (i, anim) in enumerate(self.anims):
            if is_empty_anim(anim):
                continue
            start_position = anim.start_position()
            end_position = anim.end_position()
            if (start_position <= position < end_position) or \
                (start_position == position and start_position == end_position):
                self.set_active_lbl(i)
                self.gui_window.change_panel_anim(anim)
            else:
                self.set_inactive_lbl(i)

    def add_anim(self, index):
        self.gui_window.add_empty_anim(index)
