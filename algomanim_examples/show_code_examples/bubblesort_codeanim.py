from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class DefaultBubbleSortScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [25, 43, 5])
        swaps_made = True
        while swaps_made:
            swaps_made = False
            for i in range(algolist.len() - 1):
                j = i + 1
                if algolist.compare(i, j, text=True):
                    swaps_made = True
                    algolist.swap(i, j)

    def preconfig(self, settings):
        settings['show_code'] = True

    def customize(self, action_pairs):
        self.add_complexity_analysis_line(4, position=2*DOWN)
        self.add_complexity_analysis_fn('compare', position=3*DOWN)
