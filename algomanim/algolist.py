# pylint: disable=E0602,E1101
from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.settings import Shape

class AlgoListNode:
    def __init__(self, scene, val):
        self.scene = scene
        self.node_color = scene.settings['node_color']
        self.highlight_color = scene.settings['highlight_color']
        self.node_length = scene.settings['node_size']
        self.node = {
            Shape.CIRCLE: Circle(
                color=self.node_color,
                fill_opacity=1,
                radius=self.node_length / 2,
            ),
            Shape.SQUARE: Square(
                fill_color=self.node_color,
                fill_opacity=1,
                side_length=self.node_length
            ),
            Shape.SQUIRCLE: RoundedRectangle(
                height=self.node_length,
                width=self.node_length,
                fill_color=self.node_color,
                fill_opacity=1
            )
        }[scene.settings['node_shape']]
        self.val = val
        self.txt = TextMobject(str(val))
        self.txt.set_color(scene.settings['font_color'])

        self.grp = VGroup(self.node, self.txt)

    def set_right_of(self, node):
        action = AlgoSceneAction(self.grp.next_to, AlgoTransform([node.grp, RIGHT]))
        self.scene.add_action_pair(action, action, animated=False)

    def show(self, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.add, AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def hide(self, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.remove,
            AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def highlight(self, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.node.set_fill, self.highlight_color],
                          transform=ApplyMethod, color_index=1),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(
            self.node.set_fill,
            AlgoTransform([self.highlight_color], color_index=0)
        )

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def dehighlight(self, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [self.node.set_fill, self.node_color],
                transform=ApplyMethod,
                color_index=1
            ),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(
            self.node.set_fill,
            AlgoTransform([self.node_color], color_index=0)
        )

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def static_swap(self, node):
        self_center = self.grp.get_center()
        node_center = node.grp.get_center()
        self.grp.move_to(node_center)
        node.grp.move_to(self_center)

    def swap_with(self, node, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp, node.grp], transform=CyclicReplace),
            AlgoTransform([node.grp, self.grp], transform=CyclicReplace),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.static_swap, AlgoTransform([node]))

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

class AlgoList:
    def __init__(self, scene, arr):
        # make nodes
        self.scene = scene
        self.nodes = [AlgoListNode(scene, val) for val in arr]

        # arrange nodes in order
        for i in range(1, len(self.nodes)):
            self.nodes[i].set_right_of(self.nodes[i - 1])

        # group nodes together
        self.group()
        self.center(animated=False)
        self.show(animated=False)

    def swap(self, i, j, animated=True):
        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], animated)

    def compare(self, i, j, animated=True):
        self.dehighlight(*list(range(len(self.nodes))), animated=animated)
        self.highlight(i, j, animated=animated)
        return self.get_val(i) < self.get_val(j)

    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    def center(self, animated=True):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction(self.grp.center)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def show(self, animated=True):
        for node in self.nodes:
            node.show(animated)

    def hide(self, animated=True):
        for node in self.nodes:
            node.hide(animated)

    def highlight(self, *indexes, animated=True):
        first = True
        for index in indexes:
            if first:
                self.nodes[index].highlight(animated)
                first = False
            else:
                self.nodes[index].highlight(animated, w_prev=True)

    def dehighlight(self, *indexes, animated=True):
        first = True
        for index in indexes:
            if first:
                self.nodes[index].dehighlight(animated)
                first = False
            else:
                self.nodes[index].dehighlight(animated, w_prev=True)

    def get_val(self, index, animated=False):
        if animated:
            self.highlight(index)
        return self.nodes[index].val

    def len(self):
        return len(self.nodes)

    def append(self, val, animated=True):
        node = AlgoListNode(self.scene, val)
        if self.len() > 0:
            node.set_right_of(self.nodes[-1])
        self.nodes.append(node)

        node.show(animated)
        self.group()
        self.center(animated=False)

    def pop(self, i=None, animated=True):
        if i is None:
            i = self.len()-1
        elif i < 0 or i >= self.len():
            return
        left_node = self.nodes[i - 1] if i != 0 else None
        right_nodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        self.nodes[i].hide(animated)
        self.nodes.remove(self.nodes[i])
        self.group()

        if right_nodes is not None and left_node is not None:
            # gap only needs to be closed if there are nodes on the left and right
            # if not, simply centering the remaining list would be enough
            right_grp = VGroup(*[node.grp for node in right_nodes])

            anim_action = self.scene.create_play_action(
                AlgoTransform([right_grp.next_to, left_node.grp, RIGHT], transform=ApplyMethod)
            )
            static_action = AlgoSceneAction(right_grp.set_right_of, AlgoTransform([left_node]))

            self.scene.add_action_pair(anim_action, static_action, animated=animated)

    def slice(self, start, stop, step=1, animated=True):
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()
        self.highlight(*range(start, stop, step), animated=animated)

        subvals = [n.val for n in self.nodes][start:stop:step]
        sublist = AlgoList(self.scene, subvals)

        action = AlgoSceneAction(sublist.grp.align_to, *[self.nodes[start].grp, LEFT])
        self.scene.add_action_pair(action, action, animated=animated)

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [sublist.grp.shift, DOWN * 1.1 * self.nodes[0].node_length],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction(sublist.grp.shift,
            AlgoTransform([DOWN * 1.1 * self.nodes[0].node_length]))
        self.scene.add_action_pair(anim_action, static_action, animated=animated)
        return sublist

    def concat(self, other_list, animated=True):
        self.nodes += other_list.nodes

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [other_list.grp.next_to, self.grp, RIGHT],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction(other_list.grp.next_to, AlgoTransform([self.grp, RIGHT]))

        self.scene.add_action_pair(anim_action, static_action, animated=animated)
        self.group()
