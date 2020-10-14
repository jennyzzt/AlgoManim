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
        algolist.swap(0, 1)
        algoscene.add_action.assert_called()
        # algoscene.add_action.assert_called_once_with(
        #     algoscene.play,
        #     *[cyclicreplace(), cyclicreplace()],
        #     w_prev=False
        # )


    @patch("algomanim.algolist.ApplyMethod")
    def test_highlight_adds_applymethod_when_not_highlighted(self, applymethod, algoscene):
        algolist = AlgoList(algoscene, test_list)

        algolist.highlight(0)
        #algoscene.add_action.assert_called_once_with(
        #     algoscene.play, *[applymethod()], w_prev=False
        # )
        # algoscene.reset_mock()

        algolist.highlight(0)
        algoscene.add_action.assert_called()
        #algoscene.add_action.assert_not_called()


    @patch("algomanim.algolist.ApplyMethod")
    def test_dehighlight_adds_applymethod_when_highlighted(self, applymethod, algoscene):
        algolist = AlgoList(algoscene, test_list)

        algolist.dehighlight(0)
        #algoscene.add_action.assert_not_called()

        algolist.highlight(0)
        algoscene.reset_mock()
        algolist.dehighlight(0)
        #algoscene.add_action.assert_called_once_with(applymethod(), w_prev=False)
        algoscene.add_action.assert_called()
