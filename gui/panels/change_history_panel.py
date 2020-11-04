from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel

class ChangeHistoryPanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.change_box_index = dict()
        self.change_box_list = QVBoxLayout()
        self.change_box_list.setContentsMargins(0, 0, 0, 0)

    @staticmethod
    def create_change_box(anim_change):
        anim_desc = anim_change.change_name
        change_desc = f'Change {anim_change.change_type.name.lower()} to: '

        # Create box
        change_box = QGroupBox()
        change_box.setStyleSheet("margin-top: 6px")
        # change_box.setCheckable(True) # not fully supported

        # Set layout
        change_box_layout = QHBoxLayout()
        change_box.setLayout(change_box_layout)

        # Add title label
        change_box_layout.addWidget(QLabel(anim_desc))

        # Add widgets
        change_box_layout.addWidget(QLabel(change_desc))
        widget = anim_change.change_type.get_widget()
        input_widget = anim_change.change_type.wrap_input_widget(widget)
        input_widget.set_value(anim_change.get_value())
        read_only_widget = input_widget.get_widget()
        read_only_widget.setEnabled(False)
        change_box_layout.addWidget(read_only_widget)

        return change_box

    def update_view(self):
        change_group_box = QGroupBox()
        change_group_box.setStyleSheet("border-style: none")
        change_group_box.setLayout(self.change_box_list)
        self.scroll_area.setWidget(change_group_box)

    def update_change(self, anim_change):
        # delete previous change with this anim key
        anim_key = (anim_change.action_pair_index,
                    anim_change.change_type)
        prev_change_box_index = self.change_box_index[anim_key]
        self.change_box_list.takeAt(prev_change_box_index) \
                            .widget().deleteLater()

        # update indexes in change_box_index
        for key in self.change_box_index:
            if self.change_box_index[key] > prev_change_box_index:
                self.change_box_index[key] -= 1

        # add new change
        self.add_change(anim_change)

    def add_change(self, anim_change):
        change_box = self.create_change_box(anim_change)
        key = (anim_change.action_pair_index, anim_change.change_type)
        self.change_box_index[key] = self.change_box_list.count()
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
