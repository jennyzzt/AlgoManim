# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [2, 4, 1, 3, 5])

        left_list = algolist.slice(0, 2, move=LEFT)
        right_list = algolist.slice(2, 5, move=RIGHT, shift=True, shift_vec=UP)

        algolist.merge(left_list, right_list)
