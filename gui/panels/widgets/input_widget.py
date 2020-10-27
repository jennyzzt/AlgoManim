from abc import ABC, abstractmethod

# pylint: disable=too-few-public-methods
class InputWidget(ABC):

    def __init__(self):
        super()

    @abstractmethod
    def get_value(self):
        pass
