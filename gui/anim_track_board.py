from PyQt5.QtWidgets import *

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

    def create_change_box(self, anim):
        anim_desc = f'Anim {anim["start_index"] + 1}' \
            if anim['start_index'] == anim['end_index'] \
            else f'Anim {anim["start_index"] + 1} - {anim["end_index"] + 1}'
        change_desc = 'Change Color'

        # Create change box
        change_box = QGroupBox(f'{anim_desc}: {change_desc}')
        change_box.setCheckable(True)

        # Set layout
        change_box_layout = QHBoxLayout()
        change_box.setLayout(change_box_layout)

        return change_box

    def update_view(self):
        change_group_box = QGroupBox()
        change_group_box.setStyleSheet("border-style: none")
        change_group_box.setLayout(self.change_box_list)
        self.scroll_area.setWidget(change_group_box)

    def add_change(self, anim):
        self.changes.append(anim)
        change_box = self.create_change_box(anim)
        self.change_box_list.addWidget(change_box)
        self.update_view()

    def apply_changes(self):
        print(f'{len(self.changes)} changes applied')
