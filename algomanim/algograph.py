import numpy as np
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import attach_metadata

class AlgoGraph:
    def __init__(self, scene, graph, show=False, animated=False):
        self.scene = scene
        self.graph = self.dic_to_algograph(graph)
        if show:
            self.show(animated=animated)

    def dic_to_algograph(self, graph):
        algograph = {}
        for key in graph:
            algograph[key] = AlgoGraphNode(self.scene, algograph, key, graph[key])
        return algograph

    @attach_metadata
    def show(self, metadata=None, animated=True):
        self.arrange_nodes()
        self.show_nodes(metadata, animated)
        self.show_lines(metadata, animated=animated)

    def arrange_nodes(self):
        if AlgoGraphNode.n_id > 0:
            angle = 2 * np.pi / (AlgoGraphNode.n_id)

            for key in self.graph:
                node = self.graph[key]
                new_angle = angle*node.n_id
                node.grp.move_to(2*np.array([np.cos(new_angle), np.sin(new_angle), 0]))

    def show_nodes(self, metadata=None, animated=True, w_prev=False):
        for node_key in self.graph:
            self.graph[node_key].show(metadata=metadata, animated=animated, w_prev=w_prev)
            if not w_prev:
                w_prev = True

    def show_lines(self, metadata=None, animated=True, w_prev = False):
        line_done = {}
        for node_key in self.graph:
            self.graph[node_key].show_lines(line_done, metadata, animated=animated, w_prev=w_prev)
            if not w_prev:
                w_prev = True


class AlgoGraphNode(AlgoNode):
    n_id = 0
    def __init__(self, scene, graph, val, adjs):
        self.graph = graph
        self.adjs = adjs
        self.n_id = AlgoGraphNode.n_id
        AlgoGraphNode.n_id += 1
        super().__init__(scene, val)

    def show_lines(self, line_done, metadata=None, animated=True, w_prev=False):
        if self.adjs is not None:
            for adj in self.adjs:
                if adj not in line_done or self.val not in line_done[adj]:
                    if adj not in line_done:
                        line_done[adj] = [self.val]
                    elif self.val not in line_done[adj]:
                        line_done[adj].append(self.val)

                    if self.val not in line_done:
                        line_done[self.val] = [adj]
                    elif adj not in line_done[self.val]:
                        line_done[self.val].append(adj)

                    self.add_line(self.graph[adj], metadata=metadata,
                                                 animated=animated, w_prev=w_prev)
