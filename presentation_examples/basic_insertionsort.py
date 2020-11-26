# pylint: disable = W0201
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class InsertionSortScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [25, 16, 39, 44, 5, 1])

        for i in range(algolist.len()):
            for j in range(0, i):
                if algolist.compare(i, j, text=True):
                    algolist.swap(i, j)
