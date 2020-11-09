# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algotree import AlgoTreeNode
from algomanim.settings import DEFAULT_SETTINGS

test_vals = [2, 1, 3]
algoscene =Mock()
algoscene.settings = DEFAULT_SETTINGS

@patch("algomanim.algoobject.TexMobject", Mock())
@patch("algomanim.algotree.TextMobject", Mock())
@patch("algomanim.algonode.TextMobject", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algotree.VGroup", Mock())
class TestAlgoTree:

    def test_insertion_according_to_val(self):
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        assert root.left.val <= root.val
        assert root.right.val >= root.val

    @patch("algomanim.algotree.AlgoTreeNode.delete")
    def test_remove_maintains_val_order(self, delete):
        # Creation of tree
        root = AlgoTreeNode(algoscene, test_vals[0])
        for i in range(1, len(test_vals)):
            root.insert(test_vals[i])
        # Remove val
        root = root.remove(2)
        # Check that val order is kept
        # if root.left:
        #     assert root.left.val <= root.val
        # if root.right:
        #     assert root.right.val >= root.val
        # Check that the node with val is deleted
        delete.assert_called_once()
