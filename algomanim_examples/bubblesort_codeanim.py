import inspect
from pylatexenc.latexencode import unicode_to_latex
from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class BubbleSortCodeScene(AlgoScene):
    def algoconstruct(self):
        # get algo source lines
        source_lines, _ = inspect.getsourcelines(self.algo)

        # get and remove redundant leading spaces
        tab_spacing = (len(source_lines[0]) - len(source_lines[0].lstrip())) * 2
        source_lines = [line[tab_spacing:] for line in source_lines]

        # insert pin at every alternate source line
        modified_source_lines = []
        for i, line in enumerate(source_lines):
            if i == 0:
                # do not execute first def line
                continue
            # get suitable line tab for new code line
            line_tab = ' ' * (len(line) - len(line.lstrip()))
            # strip current code line of EOL to be added into pin
            stripped_line = line.rstrip('\n')
            # add pin line then add original code line
            pin_line = f'{line_tab}self.insert_pin(\'__code__\', \'{stripped_line}\')\n'
            modified_source_lines.append(pin_line)
            modified_source_lines.append(line)

        # get modified source code and execute
        modified_source_str = ''.join(modified_source_lines)
        exec(f'{modified_source_str}')

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

    def customize(self, action_pairs):
        # add code anim text
        code_pins = self.find_pin('__code__')
        for pin in code_pins:
            index = pin.get_index()
            text = unicode_to_latex(pin.get_args()[0])
            textobj = TextMobject(text)
            self.add_transform(index, lambda: FadeIn(textobj))
