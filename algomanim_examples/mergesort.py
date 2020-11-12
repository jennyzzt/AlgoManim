# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [4, 3, 1, 4])

        self.mergesort(algolist)

    def mergesort(self, algolist):
        if algolist.len() > 1:
            # find middle index
            mid_pt = algolist.len() // 2  # 2

            # slice list into two
            left = algolist.slice(0, mid_pt, move=LEFT, shift=True)
            right = algolist.slice(mid_pt, algolist.len(), move=RIGHT)

            left = self.mergesort(left)
            right = self.mergesort(right)

            merged_list = algolist.merge(left, right, replace=True, shift=True, shift_vec=DOWN)
            merged_list.replace(algolist)

            return merged_list

        return algolist
