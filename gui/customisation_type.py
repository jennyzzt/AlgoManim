from enum import Enum
from PyQt5.QtWidgets import QLineEdit
from gui.color_button import ColorButton

class CustomisationType(Enum):

    def __init__(self, value, name, get_widgets):
        super().__init__()
        self._value_ = value
        self._name_ = name
        self.get_widgets = get_widgets

    @staticmethod
    def get_change_color_widgets():
        return [ColorButton()]

    @staticmethod
    def get_change_runtime_widgets():
        return [QLineEdit()]


    COLOR = (0, 'color', get_change_color_widgets.__get__(Enum))
    RUNTIME = (1, 'runtime', get_change_runtime_widgets.__get__(Enum))
