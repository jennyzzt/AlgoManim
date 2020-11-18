from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algograph import AlgoGraph

class AlgoGraphScene(AlgoScene):
    def preconfig(self, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = 'circle'
        settings['highlight_color'] = "#e74c3c" # red

    def algo(self):
        graph = { 'A' : [ 'B', 'C', 'F', 'G' ],
                  'B' : [ 'A', 'C', 'D', 'G' ],
                  'C' : [ 'A', 'B', 'G' ],
                  'D' : [ 'B', 'G' ],
                  'E' : [ ],
                  'F' : [ 'A', 'G' ],
                  'G' : [ 'A', 'B', 'C', 'D', 'F' ] }

        AlgoGraph(self, graph, animated=True)
