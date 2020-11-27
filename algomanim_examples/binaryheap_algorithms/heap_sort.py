from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algobinaryheap import AlgoBinaryHeap
from algomanim.algolist import AlgoList

class HeapSort(AlgoScene):

    # pylint: disable=W0613
    def algo(self):
        self.insert_pin("start_build_heap")
        heap = AlgoBinaryHeap(self, [6, 5, 4, 3, 2, 1], heap_type="min-heap")

        self.insert_pin("finished_build_heap")
        sorted_list = AlgoList(self, [], displacement=3.5 * DOWN)
        self.insert_pin("pop_off_items")
        while heap.peek() is not None:
            self.insert_pin("top_element", heap.peek_item())
            val = heap.pop()
            sorted_list.append(val)
        self.insert_pin("algorithm_finished")

    def preconfig(scene, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c"  # red

    def customize(self, action_pairs):

        # I want to have a introduction title before I start the algorithm
        start_build_heap = self.find_pin("start_build_heap")[0]
        bh_idx = start_build_heap.get_index()
        title_text = self.add_text("First build a Min-heap of the list", bh_idx, position=2 * UP)
        self.add_wait(bh_idx + 1, wait_time=0.25)

        # I want to change the title when i finish building the heap
        finished_build_heap = self.find_pin("finished_build_heap")[0]
        fbp_idx = finished_build_heap.get_index()

        title_text = self.change_text("We have finished building the heap", title_text, fbp_idx)
        self.add_wait(fbp_idx + 1, wait_time=1)

        # I want to change the title when I start to build the sorted list
        start_popping = self.find_pin("pop_off_items")[0]
        sp_idx = start_popping.get_index()

        title_text = self.change_text("Pop off the elements one by one", title_text, sp_idx)

        # I want to say that we have ended
        finished = self.find_pin("algorithm_finished")[0]
        f_idc = finished.get_index()

        self.change_text("We have a sorted list!", title_text, f_idc)






