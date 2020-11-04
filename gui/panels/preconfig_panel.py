from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel
from gui.panels.widgets.input_color_button import InputColorButton
from gui.panels.widgets.input_dropdown import InputDropdown
from gui.panels.widgets.input_text_box import InputTextBox
from gui.panels.widgets.qcolor_button import QColorButton

from algomanim.shape import Shape


SETTINGS = ([ 
    ('background_color', InputColorButton, QColorButton),
    ('node_color', InputColorButton, QColorButton),
    ('node_shape', InputDropdown, QComboBox),
    ('node_size', InputTextBox, QLineEdit),
    ('highlight_color', InputColorButton, QColorButton),
    ('font_color', InputColorButton, QColorButton)
])


# pylint: disable=too-few-public-methods
class PreconfigPanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_menu = QVBoxLayout()

        self.title_lbl = QLabel("Customize overall animation settings")
        self.title_lbl.setAlignment(Qt.AlignHCenter)
        self.create_settings_form()
        # To show form upon render (in load_settings)
        self.form_frame.hide()

        self.save_button = QPushButton("Save changes")
        self.save_button.clicked.connect(self.save_changes)

        self.custom_menu.addWidget(self.title_lbl)
        self.custom_menu.addWidget(self.form_frame)
        self.custom_menu.addWidget(self.save_button, alignment=Qt.AlignBottom)
        self.scroll_area.setLayout(self.custom_menu)

    def create_settings_form(self):
        self.form_frame = QFrame()
        form_layout = QFormLayout()

        self.change_widgets = dict()
        for label_title, widget_wrapper, widget_class in SETTINGS:
            # Modify snake_case to Title Case
            label = QLabel(label_title.replace('_', ' ').title())
            widget = widget_class()
            form_layout.addRow(label, widget)
            self.change_widgets[label_title] = widget_wrapper(widget)
        self.form_frame.setLayout(form_layout)

    def load_settings(self, settings):
        # Initialise node shape dropdown with Shapes
        if settings['node_shape']:
            dropdown = self.change_widgets['node_shape'].get_widget()
            dropdown.clear()
            dropdown.addItems([e.name for e in Shape])
            dropdown.setCurrentText(settings['node_shape'].name)

        for label in settings:
            self.change_widgets[label].set_value(settings[label])

        self.form_frame.show()


    def save_changes(self):
        for label in self.change_widgets:
            change_widget = self.change_widgets[label]
            self.gui_window.set_settings(label, change_widget.get_value())
