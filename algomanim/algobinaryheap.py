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

        # Convert to AlgoTreeNode representation
        self.arr = self.convert_num_array()

        # Initialise the structure for the tree
        self.buildheap_tree()

        # Show the tree and build the heap through heapify
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
        print(i, ":", self.arr[i].val, j, ":", self.arr[j].val)

        # Swap children nodes first
        tempL = self.arr[i].left
        tempR = self.arr[i].right

        self.arr[i].set_left(self.arr[j].left, update_depth=False)
        self.arr[i].set_right(self.arr[j].right, update_depth=False)

        self.arr[j].set_left(tempL, update_depth=False)
        self.arr[j].set_right(tempR, update_depth=False)

        # Do a swap with the parents
        tempJParent = self.arr[j].parent

        if self.arr[i].parent is not None:
            if self.arr[i].parent.left is self.arr[i]:
                self.arr[i].parent.set_left(self.arr[j], update_depth=False)
            else:
                self.arr[i].parent.set_right(self.arr[j], update_depth=False)

        if tempJParent is not None:
            if tempJParent.left is self.arr[j]:
                tempJParent.set_left(self.arr[i], update_depth=False)
            else:
                tempJParent.set_right(self.arr[i], update_depth=False)

        # Swap nodes in list
        temp = self.arr[i]

        if self.root is self.arr[i]:
            self.root = self.arr[j]
        self.arr[i] = self.arr[j]
        if self.root is self.arr[j]:
            self.root = temp
        self.arr[j] = temp

        self.root.recursive_update_depth()

        # Animated swap
        self.arr[i].swap_with(self.arr[j], metadata=metadata, animated=animated, w_prev=w_prev)


        # tempVal = self.arr[i].val
        #
        # self.arr[i].val = self.arr[j].val
        # self.arr[j].val = tempVal
        #
        # # Swap their Manim internal representations as well
        # tempGrp = self.arr[i].grp
        # self.arr[i].grp = self.arr[j].grp
        # self.arr[j].grp = tempGrp


    @attach_metadata
    def heapify(self, i, n, metadata=None, animated=True, w_prev=False, p=False):

        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and self.arr[l].val > self.arr[largest].val:
            largest = l
        if r < n and self.arr[r].val > self.arr[largest].val:
            largest = r

        if i is not largest:
            # if p:
                # print(i, ":", self.arr[i].val, largest, ":", self.arr[largest].val)
            self.swap(i, largest, metadata=metadata, animated=animated, w_prev=w_prev)
            # if p:
            #     print("NEWVALS", i, ":", self.arr[i].val, largest, ":", self.arr[largest].val)

            self.heapify(largest, n, metadata=metadata, animated=animated, w_prev=w_prev, p=p)

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
    def pop(self, metadata=None, animated=True, w_prev=False):

        # Gracefully handle empty Heaps
        if not self.arr:
            return False

        # swap the root with last left element
        self.swap(0, -1, metadata=metadata, animated=animated, w_prev=w_prev)

        # hide the last node
        self.arr[-1].hide(metadata=metadata, animated=animated, w_prev=w_prev)

        # Update the internal representation
        self.arr = self.arr[:-1]
        self.size = len(self.arr)
        self.max_depth = ceil(log(self.size, 2)) + 1

        # heapify the root node
        self.heapify(0, self.size, metadata=metadata, animated=animated, w_prev=w_prev, p=True)
        return True

    def peek(self):
        return self.arr[0].val
