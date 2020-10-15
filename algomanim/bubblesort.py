from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class BubbleSortScene(AlgoScene):
    def algoconstruct(self):
        xs = AlgoList(self, [25, 43, 5, 18, 30])
        swaps_made = True
        while swaps_made:
            swaps_made = False        
            for i in range(xs.len() - 1):
                j = i + 1
                xs.highlight(i, j)
                if xs.get_val(i) < xs.get_val(j):
                    swaps_made = True
                    xs.swap(i, j)
                xs.dehighlight(i, j)
            xs.nodes[j].dehighlight()
