from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algotree_deprecated import AlgoTreeNode, TreeTraversalType

class BinaryTreeSortScene(AlgoScene):
    def algoconstruct(self):
        numlist = [25, 43, 5, 18, 30]
        root = AlgoTreeNode(self, numlist[0])
        root.show_tree(order=TreeTraversalType.ALL_AT_ONCE)
        for i in range(1, len(numlist)):
            root.insert(numlist[i], animated=True)
        # root.hide_tree()
