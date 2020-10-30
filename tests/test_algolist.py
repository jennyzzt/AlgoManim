# pylint: disable=R0201
from unittest.mock import patch, Mock, ANY
from algomanim.algolist import AlgoList, AlgoListMetadata
from algomanim.algoscene import AlgoScene
from algomanim.settings import DEFAULT_SETTINGS

test_list = [1, 2, 3]
algoscene = Mock()
algoscene.settings = DEFAULT_SETTINGS


@patch("algomanim.algolist.VGroup", Mock())
@patch("algomanim.algolist.TextMobject", Mock())
class TestAlgoList:
    @patch("algomanim.algolist.AlgoList.show")
    def test_constructor_calls_show(self, show):
        AlgoList(algoscene, test_list)
        show.assert_called_once()

    '''@patch("algomanim.algolist.AlgoSceneAction")
    def test_swap_adds_two_action_pairs(self, algoscene_action):
        algolist = AlgoList(algoscene, test_list)
        algoscene.reset_mock()

        algolist.swap(0, 1)
        algoscene.add_action_pair.assert_called_with(
            algoscene.create_play_action(),
            algoscene_action(),
            animated=True,
            metadata=ANY
        )

        algoscene.add_action_pair.assert_called_with(
            algoscene.create_play_action(),
            algoscene_action(),
            animated=True,
            metadata=ANY
        )'''

    @patch("algomanim.algolist.AlgoListNode.show")
    @patch("algomanim.algolist.AlgoListNode.set_right_of")
    def test_append_to_right_of_list(self, show, set_right_of):
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
    def test_pop_last_element_when_no_given_index(self, hide):
        algolist = AlgoList(algoscene, test_list)
        old_length = algolist.len()
        algolist.pop()
        new_length = algolist.len()
        assert old_length - 1 == new_length
        hide.assert_called_once()

    @patch("algomanim.algolist.AlgoListNode.hide")
    def test_pop_invalid_index_does_nothing(self, hide):
        algolist = AlgoList(algoscene, test_list)
        old_length = algolist.len()
        algolist.pop(6)
        new_length = algolist.len()
        assert old_length == new_length
        hide.assert_not_called()

    @patch("algomanim.algolist.AlgoList.highlight")
    def test_slice_outofbounds_index_get_truncated(self, highlight):
        algolist = AlgoList(algoscene, test_list)
        sublist = algolist.slice(-1, 3)
        assert sublist.len() == algolist.len()
        highlight.assert_called_once()

    '''@patch("algomanim.algolist.AlgoSceneAction")
    def test_concat_two_lists_together(self, algoscene_action):
        algolist1 = AlgoList(algoscene, test_list)
        algolist1_prevlen = algolist1.len()
        algolist2 = AlgoList(algoscene, test_list)
        algoscene.reset_mock()
        algolist1.concat(algolist2)
        assert algolist1.len() == algolist2.len() + algolist1_prevlen
        algoscene.add_action_pair.assert_called_once_with(
            algoscene.create_play_action(),
            algoscene_action(),
            animated=True,
            metadata=ANY
        )'''

    '''def test_find_index_2nd_compare(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        num_initialisation_action_pairs = len(test_algoscene.action_pairs)

        algolist.compare(0, 1)
        algolist.swap(0, 1)
        algolist.compare(1, 2)
        algolist.swap(1, 2)

        list_index = algolist.find_index(test_algoscene.action_pairs, AlgoListMetadata.COMPARE, 2)

        last_elem = num_initialisation_action_pairs + \
                    len(algolist.find_index(test_algoscene.action_pairs,
                            AlgoListMetadata.COMPARE, 1)) + \
                    len(algolist.find_index(test_algoscene.action_pairs,
                            AlgoListMetadata.SWAP, 1))

        assert last_elem == list_index[0]'''
