from math import log, ceil
from algomanim.algobinarytree import AlgoBinaryTree, AlgoBinaryTreeNode
from algomanim.metadata import attach_metadata
from algomanim.algoaction import AlgoSceneAction


class AlgoBinaryHeap(AlgoBinaryTree):

    HEAP_TYPE = {
        "min-heap": lambda m, n: m < n,
        "max-heap": lambda m, n: m > n
    }

    def __init__(self, scene, arr=[], heap_type="min-heap"):
        assert heap_type in self.HEAP_TYPE, \
            "type is not one of the following" % self.HEAP_TYPE

        self.scene = scene
        self.arr = arr
        self.size = len(arr)
        self.cmp = self.HEAP_TYPE[heap_type]
        self.root = None

        # Convert to AlgoTreeNode representation
        self.arr = self.convert_num_array()

        # Initialise the structure for the tree
        self.buildheap_tree()

        # Show the tree and build the heap through heapify
        super().__init__(scene, ceil(log(self.size, 2)), self.root, show=True)
        self.buildheap()

    def convert_num_array(self):
        return [AlgoBinaryTreeNode(self.scene, num) for num in self.arr]

    def bottom_up_heapify(self, metadata=None, animated=True, w_prev=False):
        n = len(self.arr)

        # index of last non-leaf node
        start_idx = (n - 1) // 2

        for i in reversed(range(0, start_idx + 1)):
            # perform heapify from the reverse level order
            self.heapify(i, n, metadata=metadata, animated=animated, w_prev=w_prev)

    def buildheap_tree(self):
        if self.size == 0:
            return

        self.root = self.arr[0]
        stack = [(self.root, 0)]
        while stack:
            curr, i = stack.pop()

            # Iterate over children
            lIdx = 2 * i + 1
            if lIdx < self.size:
                left = self.arr[lIdx]
                curr.set_left(left)

                stack.append((left, lIdx))

            rIdx = 2 * i + 2
            if rIdx < self.size:
                right = self.arr[rIdx]
                curr.set_right(right)

                stack.append((right, rIdx))

    @attach_metadata
    def buildheap(self, metadata=None, animated=True, w_prev=False):

        self.bottom_up_heapify(metadata=metadata, animated=animated, w_prev=w_prev)

    @attach_metadata
    def swap(self, i, j, metadata=None, animated=True, w_prev=False):

        tempVal = self.arr[i].val

        self.arr[i].val = self.arr[j].val
        self.arr[j].val = tempVal

        # Swap their Manim internal representations as well
        def swap_groups(n1, n2):
            temp = n1.grp
            n1.grp = n2.grp
            n2.grp = temp

        static_action = AlgoSceneAction.create_static_action(lambda node1, node2:
                                                             swap_groups(node1, node2),
                                                             args=[self.arr[i], self.arr[j]])

        # Animated swap
        self.arr[i].swap_with(self.arr[j], metadata=metadata, animated=animated, w_prev=w_prev)

        self.scene.add_action_pair(static_action, static_action, animated=animated)

    @attach_metadata
    def heapify(self, i, n, metadata=None, animated=True, w_prev=False):

        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and self.cmp(self.arr[l].val, self.arr[largest].val):
            largest = l
        if r < n and self.cmp(self.arr[r].val, self.arr[largest].val):
            largest = r

        if i is not largest:
            self.swap(i, largest, metadata=metadata, animated=animated, w_prev=w_prev)

            self.heapify(largest, n, metadata=metadata, animated=animated, w_prev=w_prev)

    @attach_metadata
    def pop(self, metadata=None, animated=True, w_prev=False):

        # Gracefully handle empty Heaps
        if not self.arr:
            return None

        # swap the root with last left element
        self.swap(0, -1, metadata=metadata, animated=animated, w_prev=w_prev)

        # store the value of the peek element
        peek = self.arr[-1]

        # hide the last node
        self.arr[-1].hide(metadata=metadata, animated=animated, w_prev=w_prev)

        # remove from the parent node
        i = self.size - 1
        parent_idx = (i - 1) // 2
        if parent_idx >= 0:
            if self.arr[parent_idx].left.val == self.arr[-1].val:
                self.arr[parent_idx].set_left(None)
            else:
                self.arr[parent_idx].set_right(None)

        # Update the internal representation
        self.arr = self.arr[:-1]
        self.size = len(self.arr)
        self.max_depth = ceil(log(self.size, 2)) + 1

        # heapify the root node
        self.heapify(0, self.size, metadata=metadata, animated=animated, w_prev=w_prev)
        return peek

    @attach_metadata
    def insert(self, val, metadata=None, animated=True, w_prev=False):

        # Add new value to the end of the list
        self.arr.append(AlgoBinaryTreeNode(self.scene, val))

        # Update the internal representation
        self.size = len(self.arr)
        self.max_depth = ceil(log(self.size, 2)) + 1

        i = self.size - 1
        parent_idx = (i - 1) // 2

        # Set as left child if it is missing else set as right child
        if parent_idx >= 0:
            if self.arr[parent_idx].left is None:
                self.arr[parent_idx].set_left(self.arr[-1])
            else:
                self.arr[parent_idx].set_right(self.arr[-1])

        # Show the newly inserted node
        self.arr[-1].show(self.max_depth, metadata=metadata, animated=animated, w_prev=w_prev)

        # Perform Bottom-up to satisfy heap property
        self.bottom_up_heapify(metadata=metadata, animated=animated, w_prev=w_prev)

    def peek(self):
        return self.arr[0].val
