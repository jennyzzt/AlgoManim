# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [39, 40, 41, 42, 43])
        # algolist2 = AlgoList(self, [1,2])

        algolist.slice(0, 2, move=LEFT)
        algolist.slice(2, 4, move=RIGHT)
        # left_list.slice(0,1, move=DOWN)

        # concat_list = left_list.concat(right_list)
        # right_list = algolist.slice(2, 5, move=RIGHT)

        # left_list.slice(0, 1, move=LEFT)
        # left_list.slice(1, 2, move=RIGHT)

        # algolist.slice(3, 7)
