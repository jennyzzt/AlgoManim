from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel

# pylint: disable=too-few-public-methods
class CustomisePanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initialize_random_variable = True
