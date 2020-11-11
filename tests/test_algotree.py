# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algotree import AlgoTreeNode
from algomanim.settings import DEFAULT_SETTINGS

test_vals = [3, 2, 1, 4, 5]
algoscene =Mock()
algoscene.settings = DEFAULT_SETTINGS

@patch("algomanim.algoobject.TexMobject", Mock())
@patch("algomanim.algotree.TextMobject", Mock())
@patch("algomanim.algonode.TextMobject", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algotree.VGroup", Mock())
class TestAlgoTree:

    # --------------- Show tests --------------- #
    def test_show_line_adds_action_pair(self):
        root = AlgoTreeNode(algoscene, test_vals[0])
        root.show_line()
        # Check that action pairs is created and added
        # one for showing and one for positioning
        assert algoscene.add_action_pair.call_count == 2

    @patch("algomanim.algoobject.AlgoObject.show")
    @patch("algomanim.algotree.AlgoTreeNode.show_line")
    def test_show_shows_both_node_and_line(self, show, show_line):
        root = AlgoTreeNode(algoscene, test_vals[0])
        root.show()
        # Check that both node and line are shown
        show.assert_called_once()
        show_line.assert_called_once()

    @patch("algomanim.algotree.AlgoTreeNode.show")
    def test_show_tree_shows_all_nodes(self, show):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Show tree
        root.show_tree()
        # Check that every node is hidden
        assert show.call_count == root.size()

    # --------------- Hide tests --------------- #
    def test_hide_line_adds_action_pair(self):
        root = AlgoTreeNode(algoscene, test_vals[0])
        algoscene.reset_mock()
        root.hide_line()
        # Check that action pair is created and added
        algoscene.add_action_pair.assert_called_once()

    @patch("algomanim.algoobject.AlgoObject.hide")
    @patch("algomanim.algotree.AlgoTreeNode.hide_line")
    def test_hide_hides_both_node_and_line(self, hide, hide_line):
        root = AlgoTreeNode(algoscene, test_vals[0])
        root.hide()
        # Check that both node and line are hidden
        hide.assert_called_once()
        hide_line.assert_called_once()

    @patch("algomanim.algotree.AlgoTreeNode.hide")
    def test_hide_tree_hides_all_nodes(self, hide):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Hide tree
        root.hide_tree()
        # Check that every node is hidden
        assert hide.call_count == root.size()

    # --------------- Insertion tests --------------- #
    def test_insertion_according_to_val(self):
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        self.check_tree_order(root)
        assert root.size() == len(test_vals)

    # --------------- Remove tests --------------- #
    @patch("algomanim.algotree.AlgoTreeNode.delete")
    def test_remove_leaf_node(self, delete):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Remove val
        root = root.remove(1)
        # Check that val order is kept
        self.check_tree_order(root)
        assert root.size() == len(test_vals) - 1
        # Check that the node with val is deleted
        delete.assert_called_once()

    @patch("algomanim.algotree.AlgoTreeNode.delete")
    def test_remove_middle_node(self, delete):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Remove val
        root = root.remove(root.left.val)
        # Check that val order is kept
        # self.check_tree_order(root)
        # assert root.size() == len(test_vals) - 1
        # Check that the node with val is deleted
        delete.assert_called_once()

    @patch("algomanim.algotree.AlgoTreeNode.delete")
    def test_remove_root_node(self, delete):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Remove val
        root = root.remove(root.val)
        # Check that val order is kept
        # self.check_tree_order(root)
        # assert root.size() == len(test_vals) - 1
        # Check that the node with val is deleted
        delete.assert_called_once()

    # --------------- Find tests --------------- #
    def test_find_correct_val(self):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Finds val
        val = 1
        node = root.find(val)
        assert node.val == val

    def test_find_returns_none_if_not_found(self):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Tries to find val
        val = 10
        node = root.find(val)
        assert node is None


    # --------------- Helper Test Functions --------------- #
    # Checks left child val is smaller, right child val is bigger
    def check_tree_order(self, root):
        if root.left:
            assert root.left.val <= root.val
            self.check_tree_order(root.left)
        if root.right:
            assert root.right.val >= root.val
            self.check_tree_order(root.right)
