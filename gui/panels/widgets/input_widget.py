from abc import ABC, abstractmethod


class InputWidget(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_value(self):
        pass
