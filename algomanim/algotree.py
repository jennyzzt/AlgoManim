# pylint: disable=C0103
from enum import Enum, auto
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.metadata import Metadata, AlgoListMetadata

class TreeTraversalType(Enum):
    PREORDER = auto()
    INORDER = auto()
    POSTORDER = auto()

class AlgoTreeNode(AlgoNode):
    def __init__(self, scene, val, depth=0):
        super().__init__(scene, val)
        self.left = None
        self.right = None

        # features used for positioning
        self.x = -1
        self.y = depth

    # ----- Positioning Helper Functions ----- #

    # Calculate the relative x, y coords of the nodes
    # (knuth algorithm)
    def calc_layout(self, depth=0, i=0):
        if self.left:
            i = self.left.calc_layout(depth+1, i)
            self.x = i
            self.y = depth
            i += 1
        if self.right:
            self.right.calc_layout(depth+1, i)
        return i

    # Fit the node's position to its x, y fields relative to the root
    def fit_layout(self, root):
        x_diff = self.x - root.x
        y_diff = self.y - root.y
        relative_vector = (RIGHT*x_diff+DOWN*y_diff)*self.node_length*1.1
        self.set_relative_of(root, relative_vector)
        if self.left:
            self.left.fit_layout(root)
        if self.right:
            self.right.fit_layout(root)

    # Recalculate and fit nodes to layout
    def adjust_layout(self):
        self.calc_layout()
        self.fit_layout(self)

    # --------------------------------------- #

    def show_tree(self, order=TreeTraversalType.PREORDER, animated=True):
        self.adjust_layout()
        meta = Metadata(AlgoListMetadata.SHOW)
        if order == TreeTraversalType.PREORDER:
            self.show(meta, animated)
        if self.left:
            self.left.show_tree(order, animated)
        if order == TreeTraversalType.INORDER:
            self.show(meta, animated)
        if self.right:
            self.right.show_tree(order, animated)
        if order == TreeTraversalType.POSTORDER:
            self.show(meta, animated)

    def hide_tree(self, order=TreeTraversalType.PREORDER, animated=True):
        meta = Metadata(AlgoListMetadata.HIDE)
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
        if val < curr_node.val:
            if curr_node.left is None:
                new_node = AlgoTreeNode(curr_node.scene, val)
                curr_node.left = new_node
                return
            curr_node = curr_node.left
        else:
            if curr_node.right is None:
                new_node = AlgoTreeNode(curr_node.scene, val)
                curr_node.right = new_node
                return
            curr_node = curr_node.right
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
            meta = Metadata(AlgoListMetadata.APPEND)
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
