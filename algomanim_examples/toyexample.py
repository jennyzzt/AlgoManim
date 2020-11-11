# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [2, 4, 1, 3, 5])

        # algolist2 = AlgoList(self, [1,2])

        left_list = algolist.slice(0, 2, move=LEFT)
        right_list = algolist.slice(2, 5, move=RIGHT, shift=True, shift_vec=UP)
        # left_list.concat(right_list)

        algolist.merge(left_list, right_list)

        # left_list.slice(0,1, move=DOWN)

        # concat_list = left_list.concat(right_list)
        # right_list = algolist.slice(2, 5, move=RIGHT)

        # left_list.slice(0, 1, move=LEFT)
        # left_list.slice(1, 2, move=RIGHT)

        # algolist.slice(3, 7)
