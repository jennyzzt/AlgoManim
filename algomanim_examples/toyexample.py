# pylint: skip-file

from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.algobinaryheap import AlgoBinaryHeap


class ToyScene(AlgoScene):
    def algo(self):
        # algolist = AlgoList(self, [1, 3, 5, 2, 4])

        # algolist.highlight(*[0, 2, 4])
        # algolist.pop(4)
        # left = algolist.slice(0, 5 // 2, move=LEFT, shift=True)
        # left.hide()

        heap = AlgoBinaryHeap(self, [1, 2, 3, 4, 7, 100], type="min-heap")

        # print(heap.root)
        heap.pop()
        heap.insert(200)
        heap.insert(300)

    def preconfig(self, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c" # red
