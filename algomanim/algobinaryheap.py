from math import log, ceil
from algomanim.algobinarytree import AlgoBinaryTree, AlgoBinaryTreeNode
from algomanim.metadata import attach_metadata


class AlgoBinaryHeap(AlgoBinaryTree):

    HEAP_TYPE = {
        "min-heap",
        "max-heap"
    }

    def __init__(self, scene, arr=[], type="min-heap"):
        assert type in self.HEAP_TYPE,\
            "type is not one of the following" % self.HEAP_TYPE

        self.scene = scene
        self.arr = arr
        self.size = len(arr)
        self.type = type
        self.root = None

        #  Convert to AlgoNode representation
        self.arr = self.convert_num_array()

        #  Initialise the structure for the tree
        self.buildheap_tree()

        #  Show the tree and build the heap through heapify
        super().__init__(scene, ceil(log(self.size, 2)), self.root, show=True)
        self.buildheap()

    def convert_num_array(self):
        return [AlgoBinaryTreeNode(self.scene, num) for num in self.arr]

    @attach_metadata
    def buildheap(self, metadata=None, animated=True, w_prev=False):

        n = len(self.arr)

        # index of last non-leaf node
        start_idx = (n - 1) // 2

        for i in reversed(range(0, start_idx + 1)):
            # perform heapify from the reverse level order
            self.heapify(i, n, metadata=metadata, animated=animated, w_prev=w_prev)

    @attach_metadata
    def swap(self, i, j, metadata=None, animated=True, w_prev=False):
        temp = self.arr[i]
        self.arr[i] = self.arr[j]
        self.arr[j] = temp
        self.arr[i].swap_with(self.arr[j], metadata=metadata, animated=animated, w_prev=w_prev)

    @attach_metadata
    def heapify(self, i, n, metadata=None, animated=True, w_prev=False):

        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and self.arr[l].val > self.arr[largest].val:
            largest = l
        if r < n and self.arr[r].val > self.arr[largest].val:
            largest = r

        if i is not largest:
            print(i, self.arr[i].val,  self.arr[largest].val)
            self.swap(i, largest, metadata=metadata, animated=animated, w_prev=w_prev)
            self.heapify(largest, n, metadata=metadata, animated=animated, w_prev=w_prev)

    def buildheap_tree(self):
        if self.size == 0:
            return

        self.root = self.arr[0]
        stack = []
        stack.append((self.root, 0))
        while stack:
            curr, i = stack.pop()

            # Iterate over children
            lIdx = 2 * i + 1
            if lIdx < self.size:
                left = self.arr[lIdx]
                left.set_parent(curr)
                curr.set_left(left)

                stack.append((left, lIdx))

            rIdx = 2 * i + 2
            if rIdx < self.size:
                right = self.arr[rIdx]
                right.set_parent(curr)
                curr.set_right(right)

                stack.append((right, rIdx))

    def pop(self):
        pass
