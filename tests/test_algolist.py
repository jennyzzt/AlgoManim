# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algolist import AlgoList


test_list = [1, 2, 3]

@patch("algomanim.algolist.VGroup", Mock())
@patch("algomanim.algolist.TextMobject", Mock())
@patch("algomanim.algoscene.AlgoScene")
class TestAlgoList:
    @patch("algomanim.algolist.AlgoList.show")
    def test_constructor_calls_show(self, show, algoscene):
        AlgoList(algoscene, test_list)
        show.assert_called_once()


    @patch("algomanim.algolist.CyclicReplace")
    def test_swap_adds_two_cyclicreplaces(self, cyclicreplace, algoscene):
        algolist = AlgoList(algoscene, test_list)
        algoscene.reset_mock()

        algolist.swap(0, 1)
        algoscene.add_action.assert_called_once_with(
            algoscene.play,
            cyclicreplace(), cyclicreplace(),
            w_prev=False
        )
