# pylint: disable = W0201
from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList


class InsertionSortScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [25, 16, 39, 44, 5, 1])

        for i in range(algolist.len()):
            self.insert_pin('range', algolist.nodes[0], algolist.nodes[i])
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
        # add sliding window to show sorted range
        range_pins = self.find_pin('range')
        self.custom_box = None
        for pin in range_pins:
            index = pin.get_index()
            first_node = pin.get_args()[0]
            last_node = pin.get_args()[1]
            self.add_static(index, self.update_surrounding_box, [first_node, last_node])

    def update_surrounding_box(self, first_node, last_node):
        old_box = self.custom_box
        new_box = SurroundingRectangle(VGroup(first_node.grp, last_node.grp))
        if old_box is None:
            self.add(new_box)
        else:
            self.play(ReplacementTransform(old_box, new_box))
        self.custom_box = new_box
