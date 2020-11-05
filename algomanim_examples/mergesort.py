# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [3, 1, 2, 4])

        self.mergesort(algolist)

    @staticmethod
    def mergesort(algolist):
        if algolist.len() > 1:
            # find middle index
            mid_pt = algolist.len() // 2

            # slice list into two
            left = algolist.slice(0, mid_pt, animated=True)
            right = algolist.slice(mid_pt, algolist.len(), animated=True)

            left = algolist.mergesort(left)
            right = algolist.mergesort(right)

            if left.get_val(0) < right.get_val(0):
                algolist = left.concat(right)
            else:
                algolist = right.concat(left)

        return algolist
