from gui.widgets.input_widget import InputWidget

class InputColorButton(InputWidget):

    def __init__(self, qcolor_button):
        super().__init__()
        self.qcolor_button = qcolor_button
        
    def get_value(self):
        return self.qcolor_button.get_color()
