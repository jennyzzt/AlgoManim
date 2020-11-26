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

    def preconfig(self, settings):
        settings['show_code'] = True
        settings['node_shape'] = 'circle'
        settings['node_size'] = 2
        settings['node_font'] = 'sans-serif'
        settings['highlight_color'] = "#33cccc"  # teal
