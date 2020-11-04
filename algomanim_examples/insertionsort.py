# pylint: skip-file

from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class InsertionSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 16, 39, 44, 5, 1])
        for i in range(0, algolist.len()):
            algolist.highlight(i)
            for j in range(0, i):
                if algolist.compare(i, j):
                    algolist.swap(i, j)
