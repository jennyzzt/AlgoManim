from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.settings import Shape
from algomanim.metadata import AlgoListMetadata

class FindMaxScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 43, 5, 18, 30])

        cur_max_idx = 0

        for i in range(algolist.len()):
            algolist.highlight(cur_max_idx, i)
            if algolist.compare(cur_max_idx, i, highlights=False):
                algolist.dehighlight(cur_max_idx)
                cur_max_idx = i
            else:
                algolist.dehighlight(i)

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 2.5
        settings['highlight_color'] = "#33cccc"  # teal

class BinarySearchScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, list(range(0, 31, 3)))
        val = 27
        mid_pt = 0
        first = 0
        last = algolist.len()-1
        index = -1

        while (first <= last) and (index == -1):
            algolist.dehighlight(mid_pt)
            mid_pt = (first+last)//2
            algolist.highlight(mid_pt)
            if algolist.get_val(mid_pt) == val:
                index = mid_pt
            else:
                if val < algolist.get_val(mid_pt):
                    last = mid_pt -1
                else:
                    first = mid_pt +1

        print(index)

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 1
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self, action_pairs):
        actions = AlgoList.find_action_pairs(self, 3, AlgoListMetadata.HIGHLIGHT)
        for action in actions:
            action.set_color('#ff6666')
