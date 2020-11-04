from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.panels.base_changes_panel import BaseChangesPanel

from .customisation_type import CustomisationType
from .widgets.frame_layout import FrameLayout

# pylint: disable=too-few-public-methods
class CustomisePanel(BaseChangesPanel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_menu = QVBoxLayout()
        # self.custom_menu.setContentsMargins(10, 10, 0, 0)

        self.title_lbl = QLabel("Please click on an animation to customize")
        self.title_lbl.setAlignment(Qt.AlignHCenter)

        self.inner_scroll_area = QScrollArea()
        self.inner_scroll_area.setStyleSheet("border: none")
        self.inner_scroll_widget = QWidget()
        self.inner_scroll_layout = QVBoxLayout()
        self.inner_scroll_widget.setLayout(self.inner_scroll_layout)
        self.inner_scroll_area.setWidgetResizable(True)
        self.inner_scroll_area.setWidget(self.inner_scroll_widget)

        self.menu_frame = None
        self.curr_anim = None
        self.change_widgets = dict()

        self.save_button = QPushButton("Save changes")
        self.save_button.clicked.connect(self.save_changes)

        self.custom_menu.addWidget(self.title_lbl)
        self.custom_menu.addWidget(self.inner_scroll_area)
        # self.custom_menu.addWidget(self.form_frame)
        self.custom_menu.addWidget(self.save_button, alignment=Qt.AlignBottom)
        self.scroll_area.setLayout(self.custom_menu)


    def save_changes(self):
        # for change_type in self.change_widgets:
        #     (_, change_widget) = self.change_widgets[change_type]
        #     self.gui_window.add_change(self.curr_anim, change_type, change_widget.get_value())
        pass

    def set_animation(self, anim, change_vals):
        self.curr_anim = anim
        anim_desc = anim.desc()
        self.title_lbl.setText(anim_desc)

        if self.menu_frame is not None:
            self.menu_frame.setParent(None)

        self.menu_frame = QWidget()
        menu_layout = QVBoxLayout()
        self.menu_frame.setLayout(menu_layout)

        lower_metas = anim.metadata.children
        self.change_widgets = dict()
        change_possible = False
        for (i, lower_meta) in enumerate(lower_metas):
            action_pair = lower_meta.action_pair
            collapsible_box = FrameLayout(title=lower_meta.metadata.name)
            form_layout = QFormLayout()
            for (change_type, val) in action_pair.customizations().items():
                change_possible = True
                widget = change_type.get_widget()
                wrapped_widget = change_type.wrap_input_widget(widget)
                wrapped_widget.set_value(val)
                label = QLabel(change_type.name.title())
                form_layout.addRow(label, widget)
                self.change_widgets[(i, change_type)] = (label, wrapped_widget)
            collapsible_box.addLayout(form_layout)
            menu_layout.addWidget(collapsible_box)

        self.save_button.setEnabled(change_possible)
        self.inner_scroll_layout.addWidget(self.menu_frame)
