from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel
from gui.panels.widgets.qcolor_button import QColorButton

from .customisation_type import CustomisationType

# pylint: disable=too-few-public-methods
class CustomisePanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_menu = QVBoxLayout()
        # self.custom_menu.setContentsMargins(10, 10, 0, 0)

        self.title_lbl = QLabel("Please click on an animation to customize")
        self.title_lbl.setAlignment(Qt.AlignHCenter)

        self.form_frame = QFrame()
        form_layout = QFormLayout()
        self.change_widgets = dict()
        for change_type in CustomisationType:
            widget = change_type.get_widget()
            label = QLabel(change_type.name.title())
            form_layout.addRow(label, widget)
            self.change_widgets[change_type] = (label, change_type.wrap_input_widget(widget))
        self.save_button = QPushButton("Save changes")
        self.save_button.clicked.connect(self.save_changes)
        form_layout.addWidget(self.save_button)
        self.form_frame.setLayout(form_layout)
        self.form_frame.hide()
        self.curr_anim = None

        self.custom_menu.addWidget(self.title_lbl)
        self.custom_menu.addWidget(self.form_frame)
        self.scroll_area.setLayout(self.custom_menu)

    def save_changes(self):
        for change_type in self.change_widgets:
            (_, change_widget) = self.change_widgets[change_type]
            self.gui_window.add_change(self.curr_anim, change_type, change_widget.get_value())

    def set_animation(self, anim, change_vals):
        self.curr_anim = anim
        start_index = anim['start_index']
        end_index = anim['end_index']
        anim_desc = 'Animation ' + \
                    (f'{start_index + 1}' \
                     if start_index == end_index \
                     else f'{start_index + 1} - {end_index + 1}')
        self.title_lbl.setText(anim_desc)
        change_possible = False
        for change_type in CustomisationType:
            (change_label, change_widget) = self.change_widgets[change_type]
            if change_type in anim["customisations"]:
                change_possible = True
                val = change_vals[change_type]
                change_label.show()
                change_widget.get_widget().show()
                change_widget.set_value(val)
            else:
                change_label.hide()
                change_widget.get_widget().hide()

        self.save_button.setEnabled(change_possible)

        self.form_frame.show()
