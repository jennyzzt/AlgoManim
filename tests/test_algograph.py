# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algograph import AlgoGraph
from algomanim.settings import DEFAULT_SETTINGS

algoscene = Mock()
algoscene.settings = DEFAULT_SETTINGS

test_graph1 = { 'A' : [ 'B', 'C' ],
              'B' : [ 'A', 'C'],
              'C' : [ 'A', 'B' ],
              'D' : [] }

@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algograph.VGroup", Mock())
@patch("algomanim.algobinarytree.TextMobject", Mock())
@patch("algomanim.algoscene.TextMobject", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
class TestAlgoGraph:

    # --------------- Show tests --------------- #
    def test_empty_graph_no_action_pairs(self):
        algoscene.reset_mock()
        AlgoGraph(self, {}, show=True, animated=True)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 0

    def test_non_empty_graph_adds_action_pairs(self):
        algoscene.reset_mock()
        AlgoGraph(self, test_graph1, show=True, animated=True)
        # Check that only one action pair is created
        assert algoscene.add_action_pair.call_count == 10
