# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class ToyScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [1, 3, 5, 2, 4])

        left_list = algolist.slice(0, 3, move=LEFT)
        # print([n.val for n in left_list.nodes])
        right_list = algolist.slice(3, 5, move=RIGHT, shift=True, shift_vec=UP)
        # print([n.val for n in right_list.nodes])

        algolist.merge(left_list, right_list, replace=False)
