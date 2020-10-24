from enum import Enum

from PyQt5.QtWidgets import QLineEdit

from gui.widgets.input_color_button import InputColorButton
from gui.widgets.input_text_box import InputTextBox
from gui.widgets.qcolor_button import QColorButton

class CustomisationType(Enum):

    def __init__(self, value, name, get_widgets, wrap_input_widget, input_widget_index=0):
        super().__init__()
        self._value_ = value
        self._name_ = name
        self.get_widgets = get_widgets
        self.wrap_input_widget = wrap_input_widget
        self.input_widget_index = input_widget_index

    @staticmethod
    def get_change_color_widgets():
        return [QColorButton()]

    @staticmethod
    def get_change_runtime_widgets():
        return [QLineEdit()]

    COLOR = (
        0,
        'color',
        get_change_color_widgets.__get__(Enum),
        InputColorButton
    )
    RUNTIME = (
        1,
        'runtime',
        get_change_runtime_widgets.__get__(Enum),
        InputTextBox
    )
