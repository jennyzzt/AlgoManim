from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel
from .customisation_type import CustomisationType

# pylint: disable=too-few-public-methods
class CustomisePanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_menu = QVBoxLayout()
        # self.custom_menu.setContentsMargins(10, 10, 0, 0)

        self.anim_lbl = QLabel("Please click on an animation to customize")
        self.anim_lbl.setAlignment(Qt.AlignHCenter)

        self.anim_layouts = dict()
        self.curr_form_layout = None
        self.curr_anim = None
        self.change_widgets = None

        self.custom_menu.addWidget(self.anim_lbl)
        self.scroll_area.setLayout(self.custom_menu)

    def save_changes(self):
        for (change_type, input_widget) in self.change_widgets:
            self.gui_window.add_change(self.curr_anim, change_type, input_widget)

    def set_animation(self, anim):
        anim_key = anim["start_index"]
        self.curr_anim = anim

        if anim_key in self.anim_layouts:
            form_layout = self.anim_layouts[anim_key]
        else:
            form_layout = QFormLayout()
            self.change_widgets = []
            for change_type in CustomisationType:
                # check if change_type can be changed in animation in the first place
                widget = change_type.get_widget()
                input_widget = change_type.wrap_input_widget(widget)
                self.change_widgets.append((change_type, input_widget))
                form_layout.addRow(QLabel(change_type.name.title()),
                    widget)
            self.anim_layouts[anim_key] = form_layout

            save_button = QPushButton("Save changes")
            save_button.clicked.connect(self.save_changes)
            form_layout.addRow(save_button)

        if self.curr_form_layout is not None:
            self.custom_menu.removeItem(self.curr_form_layout)

        self.curr_form_layout = form_layout
        self.custom_menu.addLayout(form_layout)
