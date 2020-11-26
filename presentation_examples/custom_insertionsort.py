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
        # settings['show_code'] = True
        settings['node_shape'] = 'circle'
        settings['node_size'] = 2
        settings['node_font'] = 'sans-serif'
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self):
        # highlight 7th compare in diff colour and add a wait
        highlight_pairs = self.find_action_pairs("compare", lower_level="highlight", occurence=7)
        for h_pair in highlight_pairs:
            h_pair.set_color('#ff7c4c')

        # fast forward 2nd to 6th compare (end is not inclusive)
        compare_pair_snd = self.find_action_pairs(
            metadata_name='compare', occurence=2
        )[0]
        compare_pair_seventh = self.find_action_pairs(
            metadata_name="compare", occurence=7
        )[0]
        self.fast_forward(compare_pair_snd.get_index(),
                          compare_pair_seventh.get_index(), speed_up=8)
