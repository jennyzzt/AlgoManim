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

            self.insert_pin("build_initial_window")
            for i in range(k):
                heap.insert(list_input[i])
                self.insert_pin('window', input.nodes[0], input.nodes[i])

            self.insert_pin("add_peek_for_each")
            res.append(heap.peek())
            self.insert_pin("build_windows")
            for i in range(k, len(list_input)):
                self.insert_pin('window', input.nodes[i-k + 1], input.nodes[i])
                heap.remove(list_input[i-k])
                heap.insert(list_input[i])
                res.append(heap.peek())

            self.insert_pin("algorithm_finished")
            return res

        sliding_window_maximum(list_input=[3, 6, 1, 8, 3, 9, 0, 1], k=3)

    def preconfig(scene, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c"  # red

    def customize(self, action_pairs):

        # I want to have a introduction title for the initial window
        bi_window = self.find_pin("build_initial_window")[0]
        bi_idx = bi_window.get_index()
        title_text = self.add_text("First build our initial subarray", bi_idx, position=2 * UP)
        self.add_wait(bi_idx + 1, wait_time=0.25)

        # I want to change the title when I first add to the result
        first_add = self.find_pin("add_peek_for_each")[0]
        fa_idx = first_add.get_index()

        title_text = self.change_text("Add the peek of each subarray!", title_text, fa_idx)
        self.add_wait(fa_idx + 1, wait_time=1)

        # I want to change the title when i start building all windows
        build_windows = self.find_pin("build_windows")[0]
        build_idx = build_windows.get_index()

        title_text = self.change_text("Create the rest of the subarrays", title_text, build_idx)
        self.add_wait(build_idx + 1, wait_time=1)

        # I want to say that we have ended
        finished = self.find_pin("algorithm_finished")[0]
        f_idc = finished.get_index()

        self.change_text("We have found the maximum of each subarray!", title_text, f_idc)

        # Add sliding window to the input list
        windows = self.find_pin('window')
        self.sub_arr = None
        for window in windows:
            index = window.get_index()
            first_node = window.get_args()[0]
            last_node = window.get_args()[1]
            self.add_static(index, self.update_surrounding_box, [first_node, last_node])\

    # ------ Helper function for my own Manim animations ----- #
    def update_surrounding_box(self, first_node, last_node):
        old_box = self.sub_arr
        new_box = SurroundingRectangle(VGroup(first_node.grp, last_node.grp))
        if old_box is None:
            self.add(new_box)
        else:
            self.play(ReplacementTransform(old_box, new_box))
        self.sub_arr = new_box

