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

    def customize(self, action_pairs):
        # demonstrating the allowed edits that can be made for animations
        # TODO: add CSS style selector so that action_pairs list is more easily
        # searchable. Hardcoding indexes is very tedious.

        # 1) color of highlight is changed for first iteration of algorithm
        highlight_indices = [15, 16, 23, 24, 30, 31, 38, 39]
        for index in highlight_indices:
            action_pairs[index].change_color(PURPLE) # pylint: disable=E0602

        # 2) animations are fast forwarded (2x speed) for second iteration
        self.fast_forward(45, 75)

        # 3) insert a wait in between animations
        self.add_wait(75)

        # TODO: insert FadeOut animation => so that skipping is not so abrupt

        # TODO: insert FadeIn animation => so that skipping is not so abrupt

        # 4) skip remaining animations from third iteration till the end
        self.skip(76)
