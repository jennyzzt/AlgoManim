from PyQt5.QtWidgets import *

# pylint: disable=too-few-public-methods
class AnimChange():

    def __init__(self, anim, change_type, input_widget=None):
        self.anim = anim
        self.change_type = change_type
        self.input_widget = input_widget

    def apply(self):
        change_value = self.input_widget.get_value()
        for action_pair in self.anim['action_pairs']:
            self.change_type.customise(action_pair)(change_value)

class AnimTrackBoard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.changes = []
        self.change_box_list = QVBoxLayout()
        self.change_box_list.setContentsMargins(0, 0, 0, 0)

        # Set up scrollbar
        self.scroll_area = QScrollArea()

        # Apply button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)

        # Arrange widget contents
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(apply_button)

        self.setLayout(main_layout)

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

    def add_change(self, anim, change_type):
        change_box, input_widget = self.create_change_box(anim, change_type)
        self.changes.append(AnimChange(anim, change_type, input_widget))
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
        self.changes = []
        self.clear_layout(self.change_box_list)

    def apply_changes(self):
        for change in self.changes:
            change.apply()
        self.reset()
