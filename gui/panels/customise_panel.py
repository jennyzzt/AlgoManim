from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.animation_bar import is_empty_anim
from gui.panels.base_changes_panel import BaseChangesPanel

from .widgets.frame_layout import FrameLayout

# pylint: disable=too-few-public-methods
class CustomisePanel(BaseChangesPanel):

    def __init__(self, parent=None, changes=None):
        super().__init__(parent)
        self.custom_menu = QVBoxLayout()

        # Title
        self.title_lbl = QLabel("Please click on an animation to customize")
        self.title_lbl.setAlignment(Qt.AlignHCenter)

        # Scroll Area for form elements
        self.inner_scroll_area = QScrollArea()
        self.inner_scroll_area.setStyleSheet("border: none")
        self.inner_scroll_widget = QWidget()
        self.inner_scroll_layout = QVBoxLayout()
        self.inner_scroll_widget.setLayout(self.inner_scroll_layout)
        self.inner_scroll_area.setWidgetResizable(True)
        self.inner_scroll_area.setWidget(self.inner_scroll_widget)

        # global variables to save changes and change form elements
        self.menu_frame = None
        self.menu_layout = None
        self.change_widgets = None
        self.changes = changes
        self.text_widgets = None

        self.save_button = QPushButton("Save changes")
        self.save_button.clicked.connect(self.save_changes)

        self.custom_menu.addWidget(self.title_lbl)
        self.custom_menu.addWidget(self.inner_scroll_area)
        self.custom_menu.addWidget(self.save_button, alignment=Qt.AlignBottom)
        self.scroll_area.setLayout(self.custom_menu)

    def save_changes(self):
        # save changes for customisations
        for (action_pair_index, change_name, change_type), (change_widget, default_val) \
            in self.change_widgets.items():
            if default_val != change_widget.get_value():
                self.gui_window.add_change(
                    action_pair_index,
                    change_name,
                    change_type,
                    change_widget.get_value()
                )
        # save changes for added text frames
        self.gui_window.add_text_change(self.text_widgets)

    def reset_frame(self, title):
        # set title
        self.title_lbl.setText(title)

        # discard old frame and reset change_widgets
        self.change_widgets = dict()
        self.text_widgets = dict()
        if self.menu_frame is not None:
            self.menu_frame.setParent(None)

        # initialize new frame
        self.menu_frame = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_frame.setLayout(self.menu_layout)

    def set_animation(self, anim): # pylint: disable=too-many-locals
        if is_empty_anim(anim):
            self.reset_frame(title = "custom")
            collapsible_box = FrameLayout(title="Text animations")
            form_layout = QFormLayout()
            collapsible_box.addLayout(form_layout)

            # Add text section
            add_text_widget = QLineEdit()
            form_layout.addRow(QLabel("Add Text"), add_text_widget)
            self.text_widgets[anim['index']] = add_text_widget

            self.menu_layout.addWidget(collapsible_box)
            self.save_button.setEnabled(True)
            self.inner_scroll_layout.addWidget(self.menu_frame)
        else:
            self.reset_frame(title=anim.desc())

            change_possible = False
            for lower_meta in anim.metadata.children:
                action_pair = lower_meta.action_pair
                action_pair_index = action_pair.get_index()
                lower_meta_name = lower_meta.meta_name
                change_name = f'{anim.desc(sep=" ")} > {lower_meta_name}'

                collapsible_box = FrameLayout(title=lower_meta_name)
                form_layout = QFormLayout()

                # for each customization available in action_pair
                for (change_type, original_val) in action_pair.customizations().items():
                    change_possible = True

                    # create input widget and set default value to last changed value
                    # or original value
                    widget = change_type.get_widget()
                    wrapped_widget = change_type.wrap_input_widget(widget)
                    change_key = (action_pair_index, change_type)
                    if change_key in self.changes:
                        wrapped_widget.set_value(self.changes[change_key].get_value())
                    else:
                        wrapped_widget.set_value(original_val)

                    form_layout.addRow(QLabel(change_type.desc), widget)

                    widget_key = (action_pair_index, change_name, change_type)
                    self.change_widgets[widget_key] = wrapped_widget, wrapped_widget.get_value()

                collapsible_box.addLayout(form_layout)
                self.menu_layout.addWidget(collapsible_box)

            self.save_button.setEnabled(change_possible)
            self.inner_scroll_layout.addWidget(self.menu_frame)
