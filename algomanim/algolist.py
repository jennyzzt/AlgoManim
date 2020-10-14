from manimlib.imports import *

class AlgoListNode:
    def __init__(self, scene, val):
        self.scene = scene
        self.sq = Square(
            fill_color=WHITE, fill_opacity=1, side_length=1.5
        )
        self.val = val
        self.txt = TextMobject(str(val))
        self.txt.set_color(BLACK)
        self.highlighted = False

        self.grp = VGroup(self.sq, self.txt)
    
    def set_right_of(self, node):
        self.grp.next_to(node.grp, RIGHT)

    def show(self, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play, *[FadeIn(self.grp)], w_prev=w_prev)
        else:
            self.scene.add_action(self.scene.add, *[self.grp], w_prev=w_prev)
    
    def hide(self, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play, *[FadeOut(self.grp)], w_prev=w_prev)
        else:
            self.scene.add_action(self.remove, *[self.grp], w_prev=w_prev)
    
    def highlight(self, animated=True, w_prev=False):
        if not self.highlighted:
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(self.sq.set_fill, RED)],
                                      w_prev=w_prev)
            else:
                self.sq.set_fill(RED, opacity=1.0)
                
        self.highlighted = True
    
    def dehighlight(self, animated=True, w_prev=False):
        if self.highlighted:
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(self.sq.set_fill, WHITE)],
                                      w_prev=w_prev)
            else:
                self.sq.set_fill(WHITE, opacity=1.0)
        
        self.highlighted = False
    
    def swap_with(self, node, animated=True, w_prev=False):
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[CyclicReplace(self.grp, node.grp),
                                    CyclicReplace(node.grp, self.grp)],
                                  w_prev=w_prev)
        # TODO: Figure out how to replace them statically (w/o animation)

class AlgoList:
    def __init__(self, scene, arr):
        # make nodes
        self.scene = scene
        self.nodes = [AlgoListNode(scene, val) for val in arr]

        # arrange nodes in order
        for i in range(1, len(self.nodes)):
            self.nodes[i].set_right_of(self.nodes[i - 1])

        # group nodes together
        self.group_and_center(animated=False)
        self.show(animated=False)
    
    def swap(self, i, j, animated=True):
        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], animated)
    
    def group_and_center(self, animated=True):
        self.grp = VGroup(*[n.grp for n in self.nodes])
        if animated:
            self.scene.add_action(self.scene.play, *[ApplyMethod(self.grp.center)])
        else:
            self.grp.center()
    
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
        self.group_and_center(animated)

    def pop(self, i=None, animated=True):
        if i is None:
            i = self.len()-1
        leftNode = self.nodes[i - 1] if i != 0 else None
        rightNodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        self.nodes[i].hide(animated)
        self.nodes.remove(self.nodes[i])

        if rightNodes is not None and leftNode is not None:
            # gap only needs to be closed if there are nodes on the left and right
            # if not, simply centering the remaining list would be enough
            rightGrp = VGroup(*[node.grp for node in rightNodes])
            if animated:
                self.scene.add_action(self.scene.play,
                                      *[ApplyMethod(rightGrp.next_to, leftNode.grp, RIGHT)])
            else:
                rightGrp.set_right_of(leftNode)
        
        self.group_and_center(animated)
        #self.nodes[0].swap_with(self.nodes[-1], animated=False)

    def slice(self, start, stop, step=1, animated=True):
        subvals = [n.val for n in self.nodes][start:stop:step]
        sublist = AlgoList(self.scene, subvals)
        
        sublist.grp.align_to(self.nodes[start].grp, LEFT)
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[ApplyMethod(sublist.grp.shift,
                                                DOWN * 1.1 * self.nodes[0].sq.side_length)])
        else:
            sublist.grp.shift(DOWN * 1.1 * self.nodes[0].sq.side_length)
        return sublist

    def concat(self, ys, animated=True):
        self.nodes += ys.nodes
        if animated:
            self.scene.add_action(self.scene.play,
                                  *[ApplyMethod(ys.grp.next_to, self.grp, RIGHT)])
        else:
            ys.grp.next_to(self.grp, RIGHT)
        self.group_and_center(animated)
        
