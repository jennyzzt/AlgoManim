# pylint: skip-file

from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [1, 3, 5, 2, 4])

        algolist.highlight(*[0, 2, 4])
        algolist.dehighlight(*[0, 2, 4])
