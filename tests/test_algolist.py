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

    @patch("algomanim.algolist.AlgoListNode.show")
    @patch("algomanim.algolist.AlgoListNode.set_right_of")
    def test_append_to_right_of_list(self, show, set_right_of, algoscene):
        algolist = AlgoList(algoscene, test_list)
        show.reset_mock()
        set_right_of.reset_mock()
        
        old_length = algolist.len()
        algolist.append(4)
        new_length = algolist.len()
        assert old_length + 1 == new_length

        show.assert_called_once()
        set_right_of.assert_called_once()
        
    @patch("algomanim.algolist.AlgoListNode.hide")
    def test_pop_last_element_when_no_given_index(self, hide, algoscene):
        algolist = AlgoList(algoscene, test_list)
        old_length = algolist.len()
        algolist.pop()
        new_length = algolist.len()
        assert old_length - 1 == new_length
        hide.assert_called_once()

        
    def test_pop_invalid_index_does_nothing(self, algoscene):
        algolist = AlgoList(algoscene, test_list)        
        old_length = algolist.len()
        algolist.pop(6)
        new_length = algolist.len()
        assert old_length == new_length

    
    @patch("algomanim.algolist.ApplyMethod")
    @patch("algomanim.algolist.AlgoList.highlight")
    def test_slice_outofbounds_index_get_truncated(self, applymethod,
                                                   highlight, algoscene):
        algolist = AlgoList(algoscene, test_list)
        sublist = algolist.slice(-1, 3)
        assert sublist.len() == algolist.len()
        highlight.assert_called_once()
        
    @patch("algomanim.algolist.ApplyMethod")
    def test_concat_two_lists_together(self, applymethod, algoscene):
        algolist1 = AlgoList(algoscene, test_list)
        algolist1_prevlen = algolist1.len()
        algolist2 = AlgoList(algoscene, test_list)
        algoscene.reset_mock()
        
        algolist1.concat(algolist2)
        assert algolist1.len() == algolist2.len() + algolist1_prevlen
        algoscene.add_action.assert_called_once_with(
            algoscene.play, applymethod()
        )
