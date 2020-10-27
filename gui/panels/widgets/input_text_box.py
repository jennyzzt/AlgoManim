from PyQt5.QtWidgets import QWidget
from gui.panels.widgets.input_widget import InputWidget

# pylint: disable=too-few-public-methods
class InputTextBox(InputWidget):

    def __init__(self, qline_edit):
        super().__init__()
        self.qline_edit = qline_edit

    def get_widget(self):
        return self.qline_edit

    def get_value(self):
        return self.qline_edit.text()

    def set_value(self, val):
        return self.qline_edit.setText(str(val))

    def read_only(self):
        return QWidget(self).setReadOnly(True)
