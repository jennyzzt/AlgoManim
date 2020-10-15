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
                algolist.highlight(i, j)
                if algolist.get_val(i) < algolist.get_val(j):
                    swaps_made = True
                    algolist.swap(i, j)
                algolist.dehighlight(i, j)
            algolist.nodes[j].dehighlight()
