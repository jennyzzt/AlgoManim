from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
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

    def custom_fade_out_transform(self):
        self.save_mobjects = self.mobjects
        return list(map(FadeOut, self.save_mobjects))

    def custom_fade_in_transform(self):
        result = list(map(FadeIn, self.save_mobjects))
        self.save_mobjects = []
        return result

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 2.5
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self, action_pairs):
        # demonstrating the allowed edits that can be made for animations

        # 1) color of highlight is changed for first iteration of algorithm
        highlight_indices = [15, 16, 23, 24, 30, 31, 38, 39]
        for index in highlight_indices:
            # pink
            action_pairs[index].change_color('#ff6666') # pylint: disable=E0602

        # 2) all animations are fast forwarded (2x speed)
        self.fast_forward(0, 75)

        # 3) insert a wait between iterations
        self.add_wait(45)

        # 4) Add Custom Transforms into the list to be executed in runtime
        self.add_transform(76, self.custom_fade_out_transform)

        # 5) skip remaining animations from third iteration till the end
        self.skip(77)

        self.add_transform(len(action_pairs), self.custom_fade_in_transform)
