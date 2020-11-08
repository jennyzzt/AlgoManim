# pylint: disable=R0903
import inspect
from collections import Counter

class Metadata:
    counter = Counter()

    def __init__(self, metadata):
        # metadata is a string
        self.metadata = metadata
        Metadata.counter[metadata] += 1
        self.fid = Metadata.counter[metadata]
        self.children = []

    @staticmethod
    # Returns metadata with the name of the function that called this
    def create_fn_metadata():
        currframe = inspect.currentframe()
        return Metadata(inspect.getouterframes(currframe, 2)[1][3])

    def add_lower(self, lowermeta):
        self.children.append(lowermeta)

    def get_all_action_pairs(self):
        return list(map(lambda lower: lower.action_pair, self.children))

    def desc(self, sep='\n'):
        return f'{self.metadata}{sep}{self.fid}'

    @staticmethod
    def reset_counter():
        Metadata.counter = Counter()

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
        val = [] if val is None \
            else filter(lambda v : v is not None, val)
        self.metadata = metadata
        self.action_pair = action_pair
        self.val = val  # list of values affected by function

    def __str__(self):
        return f'LowerMetadata(meta={self.metadata}, val={self.val}' + \
            f', action_pair={self.action_pair})'

    @staticmethod
    # Returns LowerMetadata with the name of the function that called this
    def create_fn_lmetadata(action_pair, val=None):
        currframe = inspect.currentframe()
        return LowerMetadata(inspect.getouterframes(currframe, 2)[1][3],
                           action_pair, val)
