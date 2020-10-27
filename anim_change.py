# pylint: disable=too-few-public-methods
class AnimChange:

    def __init__(self, anim, change_type, input_widget=None):
        self.anim = anim
        self.change_type = change_type
        self.input_widget = input_widget

    def apply(self):
        change_value = self.input_widget.get_value()
        for action_pair in self.anim['action_pairs']:
            self.change_type.customise(action_pair)(change_value)
