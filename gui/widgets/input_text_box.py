from gui.widgets.input_widget import InputWidget

class InputTextBox(InputWidget):

    def __init__(self, qline_edit):
        super().__init__()
        self.qline_edit = qline_edit
        
    def get_value(self):
        return self.qline_edit.text()
