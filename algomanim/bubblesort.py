from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class BubbleSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 43, 5, 18, 30])
        swaps_made = True
        while swaps_made:
            swaps_made = False
            for i in range(algolist.len() - 1):
                j = i + 1
                if algolist.compare(i, j):
                    swaps_made = True
                    algolist.swap(i, j)

        highlight1 = self.actions[15]
        highlight2 = self.actions[16]

        highlight1.change_color(PINK)
        highlight2.change_color(PINK)
