# pylint: disable=too-few-public-methods
class AnimChange:

    def __init__(self, anim, change_type, change_value):
        self.anim = anim
        self.change_type = change_type
        self.change_value = change_value

    def update_value(self, change_value):
        self.change_value = change_value

    def get_value(self):
        return self.change_value

    def apply(self):
        for action_pair in self.anim['action_pairs']:
            self.change_type.customise(action_pair)(self.change_value)
