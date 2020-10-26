from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList, AlgoListMetadata
from algomanim.settings import Shape

class BubbleSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 43])
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
        settings['highlight_color'] = "#FF0000"

    def customize(self, action_pairs):
        # demonstrating the allowed edits that can be made for animations

        # 1) color of highlight is changed for first iteration of algorithm
        highlight_indices = [15, 16, 23, 24, 30, 31, 38, 39]
        for index in highlight_indices:
            action_pairs[index].change_color(PURPLE) # pylint: disable=E0602
            
        print(AlgoList.find_frame(action_pairs, AlgoListMetadata.COMPARE, 2))

        for i, action in enumerate(action_pairs):
            if action.metadata:
                # pass
                # if len(action.metadata) > 1:
                print(i, action.metadata.uid, action.metadata.metadata)
            else:
                print(i, "NONE")
        # 2) animations are fast forwarded (2x speed) for second iteration
        self.fast_forward(45, 75)

        # 3) insert a wait in between animations
        self.add_wait(75)

        # 4) Add Custom Transforms into the list to be executed in runtime
        self.add_transform(76, self.custom_fade_out_transform)

        # 5) skip remaining animations from third iteration till the end
        self.skip(77)

        self.add_transform(len(action_pairs), self.custom_fade_in_transform)
