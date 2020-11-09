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
            left = algolist.slice(0, mid_pt, move=0, shift=True)
            right = algolist.slice(mid_pt, algolist.len(), move=0)

            left = self.mergesort(left)
            right = self.mergesort(right)

            l = 0
            r = 0
            self.shift_scene(UP)

            res = AlgoList(self, [])
            while l < left.len() and r < right.len():
                if left.get_val(l) < right.get_val(r):
                    res.append(left.get_val(l))
                    l += 1
                else:
                    res.append(right.get_val(r))
                    r += 1
            while l < left.len():
                res.append(left.get_val(l))
                l += 1
            while r < right.len():
                res.append(right.get_val(r))
                r += 1
            return res

        return algolist
