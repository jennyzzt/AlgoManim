# pylint: disable=R0903
from collections import Counter
from enum import Enum, auto

class Metadata:
    counter = Counter()

    def __init__(self, metadata):
        self.metadata = metadata
        Metadata.counter[metadata] += 1
        self.fid = Metadata.counter[metadata]
        self.children = []

    def add_lower(self, lowermeta):
        self.children.append(lowermeta)

    def get_all_action_pairs(self):
        return list(map(lambda lower: lower.action_pair, self.children))

    def __str__(self):
        return f'Metadata(meta={self.metadata}, fid={self.fid}' + \
            f', children=[{self.__print_children()}])'

    def __print_children(self):
        strings = []
        for i in self.children:
            strings.append(str(i) + ', ')
        return ''.join(strings)

class LowerMetadata:

    def __init__(self, metadata, action_pair, val=None):
        if val is None:
            val = []
        self.metadata = metadata
        self.action_pair = action_pair
        self.val = val  # list of values affected by function

    def __str__(self):
        return f'LowerMetadata(meta={self.metadata}, val={self.val}' + \
            f', action_pair={self.action_pair})'


class AlgoListMetadata(Enum):
    SWAP = auto()
    COMPARE = auto()
    CENTER = auto()
    SHOW = auto()
    HIDE = auto()
    HIGHLIGHT = auto()
    DEHIGHLIGHT = auto()
    GET_VAL = auto()
    APPEND = auto()
    POP = auto()
    SLICE = auto()
    CONCAT = auto()
    SET_RIGHT_OF = auto()
