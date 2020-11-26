from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algobinaryheap import AlgoBinaryHeap
from algomanim.algolist import AlgoList

class HeapSort(AlgoScene):

    # pylint: disable=W0613
    def algo(self):

        heap = AlgoBinaryHeap(self, [4, 3, 2, 1], heap_type="min-heap")

        self.insert_pin("finished_build_heap")
        sorted_list = AlgoList(self, [], displacement=3.5 * DOWN)

        while heap.peek() is not None:
            sorted_list.append(heap.pop())

    def preconfig(scene, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c"  # red

    def customize(self, action_pairs):
        pass



