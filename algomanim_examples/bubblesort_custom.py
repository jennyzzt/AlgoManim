from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList, AlgoListMetadata
from algomanim.settings import Shape

class CustomBubbleSortScene(AlgoScene):
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

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 2.5
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self, action_pairs):
        # demonstrating the allowed edits that can be made for animations

        # 1) color of highlight is changed for first iteration of algorithm
        highlight_pairs = AlgoList.find_action_pairs(
            self,
            1,
            AlgoListMetadata.COMPARE,
            AlgoListMetadata.HIGHLIGHT)

        for action_pair in highlight_pairs:
            action_pair.set_color('#ff6666') # pylint: disable=E0602

        # 2) all animations are fast forwarded (2x speed)
        compare_pair = AlgoList.find_action_pairs(
            self,
            10,
            AlgoListMetadata.COMPARE)[0]
        compare_index = action_pairs.index(compare_pair)
        self.fast_forward(0, compare_index - 1)

        # 3) Add Custom Transforms into the list to be executed in runtime
        self.add_fade_out_all(compare_index)

        # 4) insert a wait between iterations
        self.add_wait(compare_index + 1)

        # 5) skip remaining animations from third iteration till the end
        self.skip(compare_index + 2)

        self.add_fade_in_all(len(action_pairs))
