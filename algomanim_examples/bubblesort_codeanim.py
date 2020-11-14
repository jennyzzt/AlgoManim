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
        sourcecode = [line.replace('\n', '') for line in source_lines]
        pin_code_source = f'self.insert_pin(\'__sourcecode__\', {sourcecode})\n'
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
        # zoom camera out
        self.add_static(0, self.zoom_out)

        # show source code text
        sourcecode_pin = self.find_pin('__sourcecode__')[0]
        index = sourcecode_pin.get_index()
        sourcecode = sourcecode_pin.get_args()[0]
        textobjs = [TextMobject(unicode_to_latex(line)) for line in sourcecode]
        self.add_static(index, self.show_sourcecode, [textobjs])

        # move arrow to which code line is executed
        arrow = Arrow(ORIGIN, RIGHT)
        self.add_static(index+1, self.add_arrow_beside, [arrow, textobjs[0]])
        codeindex_pins = self.find_pin('__codeindex__')
        for pin in codeindex_pins:
            index = pin.get_index()
            codeindex = pin.get_args()[0]
            self.add_transform(index, ApplyMethod, args=[arrow.next_to,
                                                         textobjs[codeindex], LEFT])

    # zoom out scene camera to twice the width
    def zoom_out(self):
        new_center = self.camera_frame.get_right()
        self.camera_frame.set_width(self.camera_frame.get_width() * 2)
        self.camera_frame.move_to(new_center)

    # show sourcecode on the right of the zoomed out screen
    def show_sourcecode(self, textobjs):
        mid_index = len(textobjs)/2
        for i, textobj in enumerate(textobjs):
            center_of_right_screen = (self.camera_frame.get_right()
                                      + self.camera_frame.get_center()) / 2.0
            textobj.move_to(center_of_right_screen)
            textobj.shift((i - mid_index) * DOWN)
            self.add(textobj)

    def add_arrow_beside(self, arrow, textobj):
        arrow.next_to(textobj, LEFT)
        self.add(arrow)
