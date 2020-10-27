from gui.panels.widgets.input_widget import InputWidget

# pylint: disable=too-few-public-methods
class InputColorButton(InputWidget):

    def __init__(self, qcolor_button):
        super().__init__()
        self.qcolor_button = qcolor_button

    def get_value(self):
        return self.qcolor_button.get_color()
