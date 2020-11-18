import numpy as np
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
# from algomanim.metadata import Metadata

class AlgoGraph:
    def __init__(self, scene, graph, show=True):
        self.scene = scene
        self.graph = self.dic_to_algograph(graph)

        if show:
            self.show_graph(animated=True)

    def dic_to_algograph(self, graph):
        algograph = {}
        for key in graph:
            algograph[key] = AlgoGraphNode(self.scene, algograph, key, graph[key])
        return algograph

    def show_graph(self, animated=True):
        self.arrange_nodes()
        self.show_nodes(animated=animated)
        self.show_lines(animated=animated)

    def arrange_nodes(self):
        angle = 2 * np.pi / (AlgoGraphNode.n_id)

        for key in self.graph:
            node = self.graph[key]
            new_angle = angle*node.n_id
            node.grp.move_to(2*np.array([np.cos(new_angle), np.sin(new_angle), 0]))

    def show_nodes(self, animated=True):
        w_prev = False
        for node in self.graph:
            self.graph[node].show(animated=animated, w_prev=w_prev)
            if not w_prev:
                w_prev = True

    def show_lines(self, animated=True):
        w_prev = False
        line_done = {}
        for node in self.graph:
            self.graph[node].show_with_line(line_done, animated=animated, w_prev=w_prev)
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

    def show_with_line(self, line_done, metadata=None, animated=True, w_prev=False):
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

                    new_line = Line(ORIGIN, ORIGIN, stroke_width=5, color=WHITE)
                    self.lines[self.graph[adj]] = new_line

                    action = AlgoSceneAction.create_static_action(self.set_line_start_end,
                                                                            [self.graph[adj]])
                    self.scene.add_action_pair(action, action, animated=False)

                    anim_action = self.scene.create_play_action(AlgoTransform(FadeIn(new_line)),
                        w_prev=w_prev)
                    static_action = AlgoSceneAction.create_static_action(self.scene.add,
                                                                                [new_line])
                    self.scene.add_action_pair(anim_action, static_action, animated=animated)
