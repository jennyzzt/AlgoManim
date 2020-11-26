# pylint: disable = W0201
from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class InsertionSortScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [25, 16, 39, 44, 5, 1])

        self.insert_pin('intro')

        for i in range(algolist.len()):
            for j in range(0, i):
                if algolist.compare(i, j, text=True):
                    algolist.swap(i, j)

        self.insert_pin('sorted')

    def preconfig(self, settings):
        # settings['show_code'] = True
        settings['node_shape'] = 'circle'
        settings['node_size'] = 2
        settings['node_font'] = 'sans-serif'
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self):
        intro_pin = self.find_pin("intro")[0]
        text = self.add_text("Let's use insertion sort!",
                             index=intro_pin.get_index(), position=2 * UP)

        outro_pin = self.find_pin("sorted")[0]
        self.change_text("Now we have a sorted list!", old_text_object=text,
                         index=outro_pin.get_index())
