# pylint: disable=E0602,E1101
from manimlib.imports import *

class AlgoListNode:
    def __init__(self, scene, val):
        self.scene = scene
        self.square = Square(
            fill_color=WHITE, fill_opacity=1, side_length=1.5
        )
        self.val = val
        self.txt = TextMobject(str(val))
        self.txt.set_color(BLACK)
        self.highlighted = False

        self.grp = VGroup(self.square, self.txt)

    def set_right_of(self, node):
        self.scene.add_action(self.grp.next_to, *[node.grp, RIGHT])

    def show(self, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play, *[FadeIn(self.grp)], w_prev=w_prev)
        else:
            self.scene.add_action(self.scene.add, *[self.grp], w_prev=w_prev)

    def hide(self, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play, *[FadeOut(self.grp)], w_prev=w_prev)
        else:
            self.scene.add_action(self.scene.remove, *[self.grp], w_prev=w_prev)

    def highlight(self, animated=True, w_prev=False):
        if not self.highlighted:
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(self.square.set_fill, RED)],
                                      w_prev=w_prev)
            else:
                self.scene.add_action(self.square.set_fill, *[RED])

        self.highlighted = True

    def dehighlight(self, animated=True, w_prev=False):
        if self.highlighted:
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(self.square.set_fill, WHITE)],
                                      w_prev=w_prev)
            else:
                self.scene.add_action(self.square.set_fill, *[WHITE])

        self.highlighted = False

    def swap_with(self, node, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[CyclicReplace(self.grp, node.grp),
                                    CyclicReplace(node.grp, self.grp)],
                                  w_prev=w_prev)
        # Figure out how to replace them statically (w/o animation)

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

    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    def center(self, animated=True):
        if animated:
            self.scene.add_action(self.scene.play, *[ApplyMethod(self.grp.center)])
        else:
            self.scene.add_action(self.grp.center)

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
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(right_grp.next_to, left_node.grp, RIGHT)])
            else:
                self.scene.add_action(right_grp.set_right_of, *[left_node])

    def slice(self, start, stop, step=1, animated=True):
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()
        self.highlight(*range(start, stop, step), animated=animated)

        subvals = [n.val for n in self.nodes][start:stop:step]
        sublist = AlgoList(self.scene, subvals)

        self.scene.add_action(sublist.grp.align_to, *[self.nodes[start].grp, LEFT])
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[ApplyMethod(sublist.grp.shift,
                                                DOWN * 1.1 * self.nodes[0].square.side_length)])
        else:
            self.scene.add_action(sublist.grp.shift,
                                  *[DOWN * 1.1 * self.nodes[0].square.side_length])
        return sublist

    def concat(self, other_list, animated=True):
        self.nodes += other_list.nodes
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[ApplyMethod(other_list.grp.next_to, self.grp, RIGHT)])
        else:
            self.scene.add_action(other_list.grp.next_to, *[self.grp, RIGHT])
        self.group()
