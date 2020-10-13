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

    def show(self, animated=True):
        if animated:
            self.scene.play(FadeIn(self.grp))
        else:
            self.scene.add(self.grp)
    
    def hide(self, animated=True):
        if animated:
            self.scene.play(FadeOut(self.grp))
        else:
            self.scene.remove(self.grp)
    
    def highlight(self, animated=True):
        if not self.highlighted:
            if animated:
                self.scene.play(ApplyMethod(self.sq.set_fill, RED))
            else:
                self.sq.set_fill(RED, opacity=1.0)
        
        self.highlighted = True
    
    def dehighlight(self, animated=True):
        if self.highlighted:
            if animated:
                self.scene.play(ApplyMethod(self.sq.set_fill, WHITE, opacity=1.0))
            else:
                self.sq.set_fill(WHITE, opacity=1.0)
        
        self.highlighted = False
    
    def swap_with(self, node, animated=True):
        if animated:
            self.scene.play(CyclicReplace(self.grp, node.grp), CyclicReplace(node.grp, self.grp))
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
            self.scene.play(ApplyMethod(self.grp.center))
        else:
            self.grp.center()
    
    def show(self, animated=True):
        for node in self.nodes:
            node.show(animated)
    
    def hide(self, animated=True):
        for node in self.nodes:
            node.hide(animated)

    def append(self, val, animated=True):
        node = AlgoListNode(self.scene, val)
        if len(self.nodes) > 0:
            node.set_right_of(self.nodes[-1])
        self.nodes.append(node)

        node.show(animated)
        self.group_and_center(animated)

    def remove_index(self, i, animated=True):
        leftNode = self.nodes[i - 1] if i != 0 else None
        rightNodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        self.nodes[i].hide(animated)
        self.nodes.remove(self.nodes[i])

        if rightNodes is not None and leftNode is not None:
            # gap only needs to be closed if there are nodes on the left and right
            # if not, simply centering the remaining list would be enough
            rightGrp = VGroup(*[node.grp for node in rightNodes])
            if animated:
                self.scene.play(ApplyMethod(rightGrp.next_to, leftNode.grp, RIGHT))
            else:
                rightGrp.set_right_of(leftNode)
        
        self.group_and_center(animated)
        self.nodes[0].swap_with(self.nodes[-1], animated=False) 

class BubbleSortScene(Scene):
    def construct(self):
        xs = AlgoList(self, [25, 43, 5, 18, 30])
        swaps_made = True
        while swaps_made:
            swaps_made = False        
            for i in range(len(xs.nodes) - 1):
                j = i + 1
                xs.nodes[i].highlight()
                xs.nodes[j].highlight()
                if xs.nodes[j].val < xs.nodes[i].val:
                    swaps_made = True
                    xs.swap(i, j)
                xs.nodes[i].dehighlight()
            xs.nodes[j].dehighlight()