from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algotree import AlgoTreeNode

class BinaryTreeSortScene(AlgoScene):
    def algoconstruct(self):
        numlist = [25, 43, 5, 18, 30]
        root = AlgoTreeNode(self, numlist[0])
        for i in range(1, len(numlist)):
            root.insert(numlist[i])
