# pylint: disable=R0903
import inspect
from collections import Counter


def attach_metadata(func):
    def wrapped_func(*args, **kwargs):
        # retrieve metadata from arguments
        metadata = kwargs["metadata"] if "metadata" in kwargs else None

        # if metadata was not given in arguments, create it for the given function
        w_prev = kwargs["w_prev"] if "w_prev" in kwargs else False
        meta = Metadata(func.__name__, w_prev) if metadata is None else metadata

        if metadata is None:
            # set metadata argument if it was not previously set
            kwargs["metadata"] = meta

        # run function, get back result
        result = func(*args, **kwargs)

        # if metadata was created, add it to the scene
        if metadata is None and len(meta.children) > 0:
            args[0].scene.add_metadata(meta)

        return result
    return wrapped_func


class Metadata:
    counter = Counter()

    def __init__(self, meta_name, w_prev=False):
        self.meta_name = meta_name  # string

        Metadata.counter[meta_name] += 1
        self.fid = Metadata.counter[meta_name]

        self.w_prev = w_prev  # whether this animation follows the previous one

        self.children = []

    @staticmethod
    # Returns metadata with the name of the function that called this
    def check_and_create(metadata=None):
        if metadata is not None:
            # If given metadata is not None, return it
            return metadata
        currframe = inspect.currentframe()
        return Metadata(inspect.getouterframes(currframe, 2)[1][3])

    def add_lower(self, lowermeta):
        self.children.append(lowermeta)

    def get_all_action_pairs(self):
        return list(map(lambda lower: lower.action_pair, self.children))

    def desc(self, sep='\n'):
        return f'{self.meta_name}{sep}{self.fid}'

    @staticmethod
    def reset_counter():
        Metadata.counter = Counter()

    def __str__(self):
        return f'Metadata(meta={self.meta_name}, fid={self.fid}' + \
            f', children=[{self.__print_children()}])'

    def __print_children(self):
        strings = []
        for i in self.children:
            strings.append(str(i) + ', ')
        return ''.join(strings)


class LowerMetadata:

    def __init__(self, meta_name, action_pair, val=None):
        if val is None:
            # default to empty list
            val = []
        else:
            val = list(filter(lambda v: v is not None, val))
        self.meta_name = meta_name
        self.action_pair = action_pair
        self.val = val  # list of values affected by function

    def __str__(self):
        return f'LowerMetadata(meta={self.meta_name}, val={self.val}' + \
            f', action_pair={self.action_pair})'

    @staticmethod
    # Returns LowerMetadata with the name of the function that called this
    def create(action_pair, val=None):
        currframe = inspect.currentframe()
        return LowerMetadata(inspect.getouterframes(currframe, 2)[1][3],
                           action_pair, val)
