from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.settings import Shape


class FindMaxScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 40, 5, 60, 50, 80])

        cur_max_idx = 0
        self.insert_pin("max_changed", algolist.get_val(cur_max_idx))

        for i in range(1, algolist.len()):
            if algolist.compare(cur_max_idx, i):
                cur_max_idx = i
                self.insert_pin("max_changed", algolist.get_val(cur_max_idx))

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 1.5
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self, action_pairs):
        # add title to beginning
        text = TextMobject('Find Maximum Value')
        text.shift(2 * UP)
        transform = lambda: Write(text)
        self.add_transform(0, transform)

        # search for pins that were previously set
        pins = self.find_pin("max_changed")
        prev_text = text
        for pin in pins:
            # extract val from list of args
            max_val = pin.get_args()[0]

            # find index to add text transformation to
            index = pin.get_index()

            # create new text object to morph to
            new_text = TextMobject(f'Current Max Value: {max_val}')
            new_text.shift(2 * UP)

            # create transform to be run at that point
            transform = lambda old_text, new_text: \
                [FadeOut(old_text), ReplacementTransform(old_text, new_text)]
            self.add_transform(index, transform, args=[prev_text, new_text])

            prev_text = new_text


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
                if val < algolist.get_val(mid_pt): # Need compare node to value function
                    last = mid_pt -1
                else:
                    first = mid_pt +1

        print(index)

    def preconfig(self, settings):
        settings['node_shape'] = Shape.CIRCLE
        settings['node_size'] = 1
        settings['highlight_color'] = "#33cccc"  # teal

    def customize(self, action_pairs):
        actions = self.find_action_pairs(method='highlight', occurence=3)
        for action in actions:
            action.set_color('#ff6666')
