from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel

class ChangeHistoryPanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.change_box_list = QVBoxLayout()
        self.change_box_list.setContentsMargins(0, 0, 0, 0)

    @staticmethod
    def create_change_box(anim_change):
        start_index = anim_change.anim['start_index']
        end_index = anim_change.anim['end_index']
        anim_desc = 'Animation ' + \
                    (f'{start_index + 1}' \
                     if start_index == end_index \
                     else f'{start_index + 1} - {end_index + 1}')
        change_desc = f'Change {anim_change.change_type.name.lower()} to: '

        # Create box
        change_box = QGroupBox(anim_desc)
        change_box.setStyleSheet("margin-top: 6px")
        # change_box.setCheckable(True) # not fully supported

        # Set layout
        change_box_layout = QHBoxLayout()
        change_box.setLayout(change_box_layout)

        # Add widgets
        change_box_layout.addWidget(QLabel(change_desc))
        change_box_layout.addWidget(anim_change.input_widget.read_only())

        return change_box

    def update_view(self):
        change_group_box = QGroupBox()
        change_group_box.setStyleSheet("border-style: none")
        change_group_box.setLayout(self.change_box_list)
        self.scroll_area.setWidget(change_group_box)

    def add_change(self, anim_change):
        '''
        input widget exists elsewhere, anim_change object passed
        to UI to display the animation and current value of change
        '''
        change_box = self.create_change_box(anim_change)
        self.change_box_list.addWidget(change_box)
        self.update_view()

    @staticmethod
    # can move this fn to a util file later
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def reset(self):
        self.clear_layout(self.change_box_list)
