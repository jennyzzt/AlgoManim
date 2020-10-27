from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel

class ChangeHistoryPanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.change_box_list = QVBoxLayout()
        self.change_box_list.setContentsMargins(0, 0, 0, 0)

    @staticmethod
    def create_change_box(anim, change_type):
        anim_desc = 'Animation ' + \
                    (f'{anim["start_index"] + 1}' \
                         if anim['start_index'] == anim['end_index'] \
                         else f'{anim["start_index"] + 1} - {anim["end_index"] + 1}')
        change_desc = f'Change {change_type.name.lower()} to: '

        # Create change box
        change_box = QGroupBox(anim_desc)
        change_box.setStyleSheet("margin-top: 6px")
        change_box.setCheckable(True)

        # Set layout
        change_box_layout = QHBoxLayout()
        change_box.setLayout(change_box_layout)

        change_box_layout.addWidget(QLabel(change_desc))
        # Add specific widgets for this change
        widgets = change_type.get_widgets()
        input_widget = change_type.wrap_input_widget(
            widgets[change_type.input_widget_index]
        )
        for widget in widgets:
            change_box_layout.addWidget(widget)

        return change_box, input_widget

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

        '''change_box, input_widget = self.create_change_box(anim, change_type)
        self.change_box_list.addWidget(change_box)
        self.update_view()'''

    @staticmethod
    # can move this fn to a util file later
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def reset(self):
        self.clear_layout(self.change_box_list)
