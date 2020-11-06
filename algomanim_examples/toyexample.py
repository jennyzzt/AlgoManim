from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [39, 40, 41, 42, 43])

        left_list = algolist.slice(0, 2, move=LEFT)
        # right_list = algolist.slice(2, 5, move=RIGHT)
        #
        # left_list.slice(0, 1, move=LEFT)
        # left_list.slice(1, 2, move=RIGHT)

        # algolist.slice(3, 7)
