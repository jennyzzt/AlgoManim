# pylint: disable=E0602
from enum import Enum, auto
from manimlib.imports import *

class Shape(Enum):
    SQUARE = auto()
    CIRCLE = auto()
    SQUIRCLE = auto()


DEFAULT_SETTINGS = {
    'font_color': BLACK,
    'highlight_color': YELLOW,
    'node_color': WHITE,
    'node_shape': Shape.SQUARE,
    'node_size': 1.5,
}
