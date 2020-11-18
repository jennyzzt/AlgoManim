from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class DefaultBubbleSortScene(AlgoScene):
    def algo(self):
        algolist = AlgoList(self, [25, 43, 5, 18, 30])
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
        # add complexity analysis for a particular function at index
        fn_line_num = 4
        codeindex_pins = self.find_pin('__codeindex__')
        pins = list(filter(lambda pin:pin.get_args()[0]==fn_line_num, codeindex_pins))
        text = None
        for i, pin in enumerate(pins):
            index = pin.get_index()
            if text is None:
                text = self.add_text(f'Fn used: {i}', index=index, position=2*DOWN)
            else:
                text = self.change_text(f'Fn used: {i}', text, index=index, position=2*DOWN)
