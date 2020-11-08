# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algolist import AlgoList
from algomanim.algoscene import AlgoScene
from algomanim.settings import DEFAULT_SETTINGS

test_list = [1, 2, 3]
algoscene = Mock()
algoscene.settings = DEFAULT_SETTINGS


@patch("algomanim.algolist.VGroup", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algonode.TextMobject", Mock())
class TestAlgoList:
    @patch("algomanim.algolist.AlgoList.show_list")
    def test_constructor_calls_show(self, show_list):
        AlgoList(algoscene, test_list)
        show_list.assert_called_once()

    #@patch("algomanim.algolist.AlgoSceneAction")
    #def test_swap_adds_two_action_pairs(self, algoscene_action):
    #    algolist = AlgoList(algoscene, test_list)
    #    algoscene.reset_mock()

    #    algolist.swap(0, 1)
    #    algoscene.add_action_pair.assert_called_with(
    #        algoscene.create_play_action(),
    #        algoscene_action(),
    #        animated=True
    #    )

    #    algoscene.add_action_pair.assert_called_with(
    #        algoscene.create_play_action(),
    #        algoscene_action(),
    #        animated=True
    #    )

    @patch("algomanim.algoobject.AlgoObject.show")
    @patch("algomanim.algoobject.AlgoObject.set_next_to")
    def test_append_to_right_of_list(self, show, set_next_to):
        algolist = AlgoList(algoscene, test_list)
        show.reset_mock()
        set_next_to.reset_mock()
        old_length = algolist.len()
        algolist.append(4)
        new_length = algolist.len()
        assert old_length + 1 == new_length
        show.assert_called_once()
        set_next_to.assert_called_once()

    @patch("algomanim.algonode.AlgoNode.hide")
    def test_pop_last_element_when_no_given_index(self, hide):
        algolist = AlgoList(algoscene, test_list)
        old_length = algolist.len()
        algolist.pop()
        new_length = algolist.len()
        assert old_length - 1 == new_length
        hide.assert_called_once()

    @patch("algomanim.algonode.AlgoNode.hide")
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

    #@patch("algomanim.algolist.AlgoSceneAction")
    #def test_concat_two_lists_together(self, algoscene_action):
    #    algolist1 = AlgoList(algoscene, test_list)
    #    algolist1_prevlen = algolist1.len()
    #    algolist2 = AlgoList(algoscene, test_list)
    #    algoscene.reset_mock()
    #    algolist1.concat(algolist2)
    #    assert algolist1.len() == algolist2.len() + algolist1_prevlen
    #    algoscene.add_action_pair.assert_called_once_with(
    #        algoscene.create_play_action(),
    #        algoscene_action(),
    #        animated=True
    #    )

    def test_find_action_pairs_2nd_compare(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1, text=False)
        algolist.swap(0, 1)
        algolist.compare(1, 2,text=False)
        algolist.swap(1, 2)

        action_pairs_len = len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                          'compare'))

        sum_action_pairs = len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                          'compare', 'dehighlight')) + \
                           len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                          'compare', 'highlight'))

        assert action_pairs_len == sum_action_pairs

    def test_find_action_pairs_2nd_compare_with_lower(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1, text=False)
        algolist.swap(0, 1)
        algolist.compare(1, 2, text=False)
        algolist.swap(1, 2)

        action_pairs_len = len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                         'compare',
                                                          'dehighlight'))

        sum_action_pairs = len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                          'compare')) - \
                           len(AlgoList.find_action_pairs(test_algoscene, 2,
                                                          'compare', 'highlight'))

        assert action_pairs_len == sum_action_pairs

    def test_find_action_pairs_2nd_compare_invalid_upper(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1)
        algolist.swap(0, 1)
        algolist.compare(1, 2)
        algolist.swap(1, 2)

        action_pairs = AlgoList.find_action_pairs(test_algoscene, 2,
                                                  'highlight')

        assert len(action_pairs) == 0

    def test_find_action_pairs_2nd_compare_invalid_lower(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1)
        algolist.swap(0, 1)
        algolist.compare(1, 2)
        algolist.swap(1, 2)

        action_pairs = AlgoList.find_action_pairs(test_algoscene, 2,
                                                  'comapre',
                                                  'swap')

        assert len(action_pairs) == 0
