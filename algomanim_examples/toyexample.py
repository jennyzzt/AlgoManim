from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [39, 40, 41, 42])
        # algolist2 = AlgoList(self, [39, 40, 41, 42])
        # algolist.concat(algolist2)

        algolist.slice(0, 2)

        # algolist.compare(0, 1)
        # algolist.swap(0, 1)