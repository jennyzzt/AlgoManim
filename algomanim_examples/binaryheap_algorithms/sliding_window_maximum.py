from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algobinaryheap import AlgoBinaryHeap
from algomanim.algolist import AlgoList

class SlidingWindowMaximum(AlgoScene):

    # pylint: disable=W0613
    def algo(self):

        def sliding_window_maximum(list_input, k):

            heap = AlgoBinaryHeap(self, heap_type="max-heap")
            input = AlgoList(self, list_input, displacement=2.5 * DOWN)
            res = AlgoList(self, arr=[], displacement=3.5 * DOWN)

            for i in range(k):
                heap.insert(list_input[i])
                self.insert_pin('window', input.nodes[0], input.nodes[i])

            res.append(heap.peek())
            for i in range(k, len(list_input)):
                self.insert_pin('window', input.nodes[i-k + 1], input.nodes[i])
                heap.remove(list_input[i-k])
                heap.insert(list_input[i])
                res.append(heap.peek())

            return res

        sliding_window_maximum(list_input=[3, 6, 1, 8, 3, 9, 0, 1], k=3)

    def preconfig(scene, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c"  # red

    def customize(self, action_pairs):
        # Add sliding window to the input list
        windows = self.find_pin('window')
        self.sub_arr = None
        for window in windows:
            index = window.get_index()
            first_node = window.get_args()[0]
            last_node = window.get_args()[1]
            self.add_static(index, self.update_surrounding_box, [first_node, last_node])

    # ------ Helper functions for my own Manim animations ----- #
    def update_surrounding_box(self, first_node, last_node):
        old_box = self.sub_arr
        new_box = SurroundingRectangle(VGroup(first_node.grp, last_node.grp))
        if old_box is None:
            self.add(new_box)
        else:
            self.play(ReplacementTransform(old_box, new_box))
        self.sub_arr = new_box

