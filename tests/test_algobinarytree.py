# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algobinarytree import AlgoBinaryTree, AlgoBinaryTreeNode
from algomanim.settings import DEFAULT_SETTINGS

test_vals = [3, 2, 1, 4, 5]
algoscene =Mock()
algoscene.settings = DEFAULT_SETTINGS

@patch("algomanim.algoobject.TexMobject", Mock())
@patch("algomanim.algobinarytree.TextMobject", Mock())
@patch("algomanim.algonode.TextMobject", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algobinarytree.VGroup", Mock())
class TestAlgoTree:

    # --------------- Show tests --------------- #
    def test_root_adds_one_action_pair(self):
        algoscene.reset_mock()
        root = AlgoBinaryTreeNode(algoscene, test_vals[0])
        root.show(1)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 1

    def test_leaf_adds_3_action_pairs(self):
        algoscene.reset_mock()
        root = AlgoBinaryTreeNode(algoscene, test_vals[0])
        left_child = AlgoBinaryTreeNode(algoscene, test_vals[1])
        root.set_left(left_child)
        left_child.show(2)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 3

    def test_recursive_show_num_pairs(self):
        algoscene.reset_mock()
        root = AlgoBinaryTreeNode(algoscene, test_vals[0])
        left_child = AlgoBinaryTreeNode(algoscene, test_vals[1])
        root.set_left(left_child)
        root.recursive_show(2)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 4

    # --------------- Insertion tests --------------- #
    def test_insertion_according_to_val(self):
        algoscene.reset_mock()
        root = AlgoBinaryTreeNode(algoscene, test_vals[0])
        tree = AlgoBinaryTree(algoscene, 4, root)
        for i in range(1, len(test_vals)):
            tree.insert(test_vals[i])
        self.check_tree_order(root)
        assert tree.size() == len(test_vals)

    # --------------- Find tests --------------- #
    def test_find_adds_action_pairs(self):
        # if value is found, 2 action pairs should be added
        root = AlgoBinaryTreeNode(algoscene, test_vals[0])
        tree = AlgoBinaryTree(algoscene, 4, root)
        for i in range(1, len(test_vals)):
            tree.insert(test_vals[i])
        algoscene.reset_mock()
        root.recursive_find(2)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 2

    # --------------- Helper Test Functions --------------- #
    # Checks left child val is smaller, right child val is bigger
    def check_tree_order(self, root):
        if root.left:
            assert root.left.val <= root.val
            self.check_tree_order(root.left)
        if root.right:
            assert root.right.val >= root.val
            self.check_tree_order(root.right)
