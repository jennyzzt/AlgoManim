# pylint: disable=C0103
from enum import Enum, auto
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata
from algomanim.settings import Shape

class TreeTraversalType(Enum):
    PREORDER = auto()
    INORDER = auto()
    POSTORDER = auto()

class AlgoTreeNode(AlgoNode):
    def __init__(self, scene, val, depth=0):
        # default node configs for treenodes
        scene.settings['node_shape'] = Shape.CIRCLE

        super().__init__(scene, val)

        self.left = None
        self.right = None
        self.treegrp = None

        # features used for positioning
        self.x = -1
        self.y = depth

        # for visualisation
        #self.line = Line(ORIGIN, ORIGIN, stroke_width=10, color=WHITE)
        self.line = None


    def static_set_line_with(self, parent):
        #self.line.set_start_and_end_attrs(self.grp, parent.grp)
        self.line = Line(self.grp.get_center(), parent.grp.get_center(),
                         stroke_width=10)

    # Set the line connecting the node to its parent
    def set_line_with(self, parent):
        action = AlgoSceneAction.create_static_action(self.static_set_line_with, [parent])
        self.scene.add_action_pair(action, action, animated=False)

    # ----- Visualization Positioning Helper Functions ----- #

    # Calculate the relative x, y coords of the nodes
    # (knuth algorithm)
    def calc_layout(self, depth=0, i=0):
        # Assign x and y coords to left children nodes
        if self.left:
            i = self.left.calc_layout(depth+1, i)
        # Assign x and y coords to this node
        self.x = i
        self.y = depth
        i += 1
        # Assign x and y coords to right children nodes
        if self.right:
            i = self.right.calc_layout(depth+1, i)
        return i

    # Fit the node's position to its x, y fields relative to the root
    def fit_layout(self, parent=None):
        if parent is not None:
            x_diff = self.x - parent.x
            y_diff = self.y - parent.y
            relative_vector = (RIGHT*x_diff+DOWN*y_diff)*self.node_length
            # set node position
            self.set_relative_of(parent, relative_vector)
            # set node's line position
            self.set_line_with(parent)
        if self.left:
            self.left.fit_layout(self)
        if self.right:
            self.right.fit_layout(self)

    # Recalculate and fit nodes to layout
    def adjust_layout(self):
        self.calc_layout()
        self.fit_layout()
        self.treegroup()
    # ---------------------------------------------------- #

    # Get a list of all tree nodes with this node as the root
    def get_all_nodes(self):
        nodes = []
        nodes.append(self)
        if self.left:
            nodes += self.left.get_all_nodes()
        if self.right:
            nodes += self.right.get_all_nodes()
        return nodes

    # Treegroup all tree nodes together
    def treegroup(self):
        nodes = self.get_all_nodes()
        self.treegrp = VGroup(*[n.grp for n in nodes])

    # Center the tree on screen
    def center(self, animated=True, metadata=None):
        curr_metadata = metadata if metadata else Metadata('center')

        anim_action = self.scene.create_play_action(
            AlgoTransform([self.treegrp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction.create_static_action(self.treegrp.center)

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Create LowerMetadata
        lower_meta = LowerMetadata('center', action_pair)
        curr_metadata.add_lower(lower_meta)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(curr_metadata)

    # ------------- Show Helper Functions ------------- #

    # Show only the line connecting this node to the parent
    def show_line(self, metadata, animated=True, w_prev=False):
        if self.line is None:
            return
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.line], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.line])
        self.scene.add_action_pair(anim_action, static_action, animated=animated)
        if metadata:
            pass

    # Show both the node and the line connecting it
    def show(self, metadata, animated=True, w_prev=False):
        self.show_line(metadata, animated, w_prev)
        super().show(metadata, animated, w_prev)

    # Recursely show entire tree with this node as the root
    def recurse_show_tree(self, order, animated=True):
        meta = Metadata('show')
        if order == TreeTraversalType.PREORDER:
            self.show(meta, animated)
        if self.left:
            self.left.recurse_show_tree(order, animated)
        if order == TreeTraversalType.INORDER:
            self.show(meta, animated)
        if self.right:
            self.right.recurse_show_tree(order, animated)
        if order == TreeTraversalType.POSTORDER:
            self.show(meta, animated)
    # ---------------------------------------------------- #

    # Adjust tree structure and show
    def show_tree(self, order=TreeTraversalType.PREORDER, animated=True):
        self.adjust_layout()
        self.recurse_show_tree(order, animated)

    # Hide entire tree with this node as the root
    def hide_tree(self, order=TreeTraversalType.PREORDER, animated=True):
        meta = Metadata('hide')
        if order == TreeTraversalType.PREORDER:
            self.hide(meta, animated)
        if self.left:
            self.left.hide_tree(order, animated)
        if order == TreeTraversalType.INORDER:
            self.hide(meta, animated)
        if self.right:
            self.right.hide_tree(order, animated)
        if order == TreeTraversalType.POSTORDER:
            self.hide(meta, animated)

    def insert(self, val, animated=True):
        curr_node = self
        # If value is less than curr_node, insert to the left
        if val < curr_node.val:
            if curr_node.left is None:
                new_node = AlgoTreeNode(curr_node.scene, val)
                curr_node.left = new_node
                return
            curr_node = curr_node.left
        # Else insert to the right
        else:
            if curr_node.right is None:
                new_node = AlgoTreeNode(curr_node.scene, val)
                curr_node.right = new_node
                return
            curr_node = curr_node.right
        # curr_node is filled, try next one
        curr_node.insert(val, animated)

    # Returns the minimum value node in the tree
    def min_val_node(self):
        curr_node = self
        while curr_node.left:
            curr_node = curr_node.left
        return curr_node

    def remove(self, val, animated=True):
        if val < self.val:
            self.left = self.left.remove(val, animated)
        elif val > self.val:
            self.right = self.right.remove(val, animated)
        else:
            # found node with val to be deleted
            meta = Metadata('remove')
            if self.left is None:
                self.hide(meta, animated)
                return self.right
            if self.right is None:
                self.hide(meta, animated)
                return self.left
            # node with two children, get the inorder successor
            temp = self.right.min_val_node()
            self.val = temp.val
            # delete the inorder successor
            self.right = self.right.remove(temp.val, animated)
        return self