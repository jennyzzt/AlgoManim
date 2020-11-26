from unittest.mock import patch, Mock, ANY
from collections import Callable
from math import log, ceil
from algomanim.algobinarytree import AlgoBinaryTreeNode
from algomanim.algobinaryheap import AlgoBinaryHeap
from algomanim.settings import DEFAULT_SETTINGS

test_vals = [3, 2, 1, 4, 5]
algoscene =Mock()
algoscene.settings = DEFAULT_SETTINGS

@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algobinarytree.VGroup", Mock())
@patch("algomanim.algobinarytree.TextMobject", Mock())
@patch("algomanim.algoscene.TextMobject", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
class TestAlgoBinaryHeap:

    # -------- Construction Tests --------- #
    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.buildheap')
    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.buildheap_tree')
    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.convert_num_array')
    def test_construct_binary_tree(self, convert_num_array, buildheap_tree, buildheap):
        algoscene.reset_mock()
        _ = AlgoBinaryHeap(algoscene, arr=test_vals)

        # Convert the initial array into AlgoNodes
        convert_num_array.assert_called_once()

        # Build the tree
        buildheap_tree.assert_called_once()

        # Heapify appropriately built through heapify
        buildheap.assert_called_once()

    def test_heap_initialisation_representation(self):

        def commons(structure, heap_type):
            # Internal array are AlgoTreeNodes
            for i in structure.arr:
                assert isinstance(i, AlgoBinaryTreeNode)

            # Take instance of root
            assert isinstance(structure.root, AlgoBinaryTreeNode)

            # Uses the right comparator specified by HEAP_TYPE
            assert structure.cmp is AlgoBinaryHeap.HEAP_TYPE[heap_type]

        algoscene.reset_mock()
        heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="min-heap")
        commons(heap, "min-heap")

        algoscene.reset_mock()
        heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="max-heap")
        commons(heap, "max-heap")

    #  --------- Heap property tests --------- #
    # Helper to show heap_property is kept in the Tree representation
    def tree_heap_property_held(self, tree_node, cmp):
        if tree_node is not None:
            if tree_node.left is not None:
                assert cmp(tree_node.val, tree_node.left.val)
            if tree_node.right is not None:
                assert cmp(tree_node.val, tree_node.right.val)

            self.tree_heap_property_held(tree_node.left, cmp)
            self.tree_heap_property_held(tree_node.right, cmp)

    # Helper to show heap_property is kept in the Array representation
    def arr_heap_property_held(self, arr, cmp):
        n = len(arr)

        for i in range(n):
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n:
                assert cmp(arr[i].val, arr[l].val)
            if r < n:
                assert cmp(arr[i].val, arr[r].val)

    def heap_property_held(self, heap):
        self.tree_heap_property_held(heap.root, heap.cmp)
        self.arr_heap_property_held(heap.arr, heap.cmp)

    def test_initialisation_obeys_heap_property(self):
        algoscene.reset_mock()
        min_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="min-heap")
        self.heap_property_held(min_heap)

        algoscene.reset_mock()
        max_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="max-heap")
        self.heap_property_held(max_heap)

    def test_pop_obeys_heap_property(self):
        algoscene.reset_mock()
        min_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="min-heap")
        min_heap.pop()
        self.heap_property_held(min_heap)

        algoscene.reset_mock()
        max_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="max-heap")
        min_heap.pop()
        self.heap_property_held(max_heap)

    def test_insert_obeys_heap_property(self):
        algoscene.reset_mock()
        min_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="min-heap")
        min_heap.insert(100)
        self.heap_property_held(min_heap)

        algoscene.reset_mock()
        max_heap = AlgoBinaryHeap(algoscene, arr=test_vals, heap_type="max-heap")
        min_heap.insert(100)
        self.heap_property_held(max_heap)

    #  --------- Animation wiring tests --------- #
    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_swap_wiring(self, create_static_action):
        algoscene.reset_mock()
        heap = AlgoBinaryHeap(algoscene, arr=test_vals)
        heap.swap(0, 1)
        create_static_action.assert_called()

        # Assert that we are delaying the swap by doing a lambda
        args, _ = create_static_action.call_args
        assert isinstance(args[0], Callable)

    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.heapify')
    @patch('algomanim.algobinarytree.AlgoBinaryTreeNode.hide')
    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.swap')
    def test_pop_wiring(self, swap, hide, heapify):
        algoscene.reset_mock()
        heap = AlgoBinaryHeap(algoscene, arr=test_vals)
        heap.pop()

        # # Swap first node and last node
        swap.assert_any_call(0, -1, metadata=ANY, animated=ANY, w_prev=ANY)

        # Hide last node before removal
        hide.assert_called_once()

        # Internal representation has been updated
        assert heap.size == len(heap.arr) and heap.size == len(test_vals) - 1
        assert heap.max_depth == ceil(log(heap.size, 2)) + 1

        # heapify to maintain heap property
        heapify.assert_any_call(0, heap.size, metadata=ANY, animated=ANY, w_prev=ANY)

    @patch('algomanim.algobinaryheap.AlgoBinaryHeap.bottom_up_heapify')
    @patch('algomanim.algobinarytree.AlgoBinaryTreeNode.show')
    def test_insert_wiring(self, show, bottom_up_heapify):
        algoscene.reset_mock()
        heap = AlgoBinaryHeap(algoscene, arr=test_vals)
        heap.insert(100)

        # Hide last node before removal
        show.assert_called()

        # Internal representation has been updated
        assert heap.size == len(heap.arr) and heap.size == len(test_vals) + 1
        assert heap.max_depth == ceil(log(heap.size, 2)) + 1

        # 1st Bottom up heapify when constructing,
        # 2nd Bottom up heapify to maintain heap property after inserting
        assert bottom_up_heapify.call_count == 2
