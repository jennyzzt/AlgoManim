from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods
class InputWidget(ABC):

    def __init__(self):
        super()

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    # Returns a version of itself that is non-modifiable
    def read_only(self):
        pass