import inspect
from pylatexenc.latexencode import unicode_to_latex
from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class BubbleSortCodeScene(AlgoScene):
    def algoconstruct(self):
        # get algo source lines
        source_lines, _ = inspect.getsourcelines(self.algo)

        modified_source_lines = []

        # insert pin at the beginning to show all code
        sourcecode = ''.join([line.replace('\n', '\\n') for line in source_lines])
        pin_code_source = f'self.insert_pin(\'__codesource__\', \'{sourcecode}\')\n'
        modified_source_lines.append(pin_code_source)

        # get redundant spacing for first code line that is not def
        redundant_space_count = len(source_lines[1]) - len(source_lines[1].lstrip())
        # insert pin at every alternate source line
        for i, line in enumerate(source_lines):
            if i == 0:
                # do not execute first def line
                continue
            # get suitable line tab for new code line
            line_tab = ' ' * (len(line) - len(line.lstrip()) - redundant_space_count)
            # pin index of the code line
            pin = f'{line_tab}self.insert_pin(\'__codeindex__\', {i})\n'
            modified_source_lines.append(pin)
            # add original code back
            modified_source_lines.append(line[redundant_space_count:])

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
        code_pins = self.find_pin('__codesource__')
        print(len(code_pins))
