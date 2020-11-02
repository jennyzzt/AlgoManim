from enum import Enum, auto
from algomanim.algonode import AlgoNode
from algomanim.metadata import Metadata, AlgoListMetadata

class TreeTraversalType(Enum):
    PREORDER = auto()
    INORDER = auto()
    POSTORDER = auto()

class AlgoTreeNode(AlgoNode):
    def __init__(self, scene, val):
        super().__init__(scene, val)
        self.left = None
        self.right = None
        meta = Metadata(AlgoListMetadata.SHOW)
        self.show(meta, animated=False)

    def put_left(self, node):
        self.left = node
        node.set_down_left_of(self)

    def put_right(self, node):
        self.right = node
        node.set_down_right_of(self)

    def show_tree(self, order=TreeTraversalType.PREORDER, animated=True):
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
        meta = Metadata(AlgoListMetadata.APPEND)
        if val < self.val:
            if curr_node.left is None:
                new_node = AlgoTreeNode(self.scene, val)
                curr_node.put_left(new_node)
                new_node.show(meta, animated)
                return
            curr_node = curr_node.left
        else:
            if curr_node.right is None:
                new_node = AlgoTreeNode(self.scene, val)
                curr_node.put_right(new_node)
                new_node.show(meta, animated)
                return
            curr_node = curr_node.right
        curr_node.insert(val, animated)
