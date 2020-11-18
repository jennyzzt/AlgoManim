# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algolist import AlgoList
from algomanim.algoscene import AlgoScene
from algomanim.settings import DEFAULT_SETTINGS

test_list = [1, 2, 3]
algoscene = Mock()
algoscene.settings = DEFAULT_SETTINGS


@patch("algomanim.algolist.VGroup", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algoscene.TextMobject", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
class TestAlgoList:
    @patch("algomanim.algolist.AlgoList.show_list")
    def test_constructor_calls_show(self, show_list):
        AlgoList(algoscene, test_list)
        show_list.assert_called_once()

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

    def test_find_action_pairs_2nd_compare(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1, text=False)
        algolist.swap(0, 1)
        algolist.compare(1, 2,text=False)
        algolist.swap(1, 2)

        action_pairs_len = len(test_algoscene.find_action_pairs(method='compare', occurence=2))

        sum_action_pairs = len(test_algoscene.find_action_pairs(occurence=2, method='compare',
                                                                lower_level='dehighlight')) + \
                           len(test_algoscene.find_action_pairs(method='compare', occurence=2,
                                                                lower_level='highlight'))

        assert action_pairs_len == sum_action_pairs

    def test_find_action_pairs_2nd_compare_with_lower(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1, text=False)
        algolist.swap(0, 1)
        algolist.compare(1, 2, text=False)
        algolist.swap(1, 2)

        action_pairs_len = len(test_algoscene.find_action_pairs(method='compare', occurence=2,
                                                                lower_level='dehighlight'))

        sum_action_pairs = len(test_algoscene.find_action_pairs(method='compare', occurence=2,)) - \
                           len(test_algoscene.find_action_pairs(method='compare', occurence=2,
                                                                lower_level='highlight'))

        assert action_pairs_len == sum_action_pairs

    def test_find_action_pairs_2nd_compare_invalid_upper(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1)
        algolist.swap(0, 1)
        algolist.compare(1, 2)
        algolist.swap(1, 2)

        action_pairs = test_algoscene.find_action_pairs(method='highlight', occurence=2)

        assert len(action_pairs) == 0

    def test_find_action_pairs_2nd_compare_invalid_lower(self):
        test_algoscene = AlgoScene()
        algolist = AlgoList(test_algoscene, test_list)

        algolist.compare(0, 1)
        algolist.swap(0, 1)
        algolist.compare(1, 2)
        algolist.swap(1, 2)

        action_pairs = test_algoscene.find_action_pairs(method='compare', occurence=2,
                                                        lower_level='swap')

        assert len(action_pairs) == 0

# --------------- Slice Tests --------------- #
#     def slice_set_up(self) -> None:
#         algoscene.reset_mock()
#         self.algolist = AlgoList(algoscene, test_list)

    # Check that the internal representation is represented accordingly
    def test_slice_internal_list_same_as_list_slicing(self):
        algoscene.reset_mock()
        algolist = AlgoList(algoscene, test_list)

        for i in range(1, algolist.len() + 1):
            new_list = algolist.slice(0, i)
            assert [n.val for n in new_list.nodes] == test_list[0:i]

    # Check that a few key solutions were called
    @patch("algomanim.algolist.AlgoList.hide_list")
    def test_key_slice_internal_calls(self, hide_list):
        algoscene.reset_mock()
        algolist = AlgoList(algoscene, test_list)

        _ = algolist.slice(0, len(test_list))
        hide_list.assert_called_once()

        _ = algolist.slice(0, len(test_list), shift=True)
        algoscene.shift_scene.assert_called_once()

# --------------- Merge Tests --------------- #
#     def merge_set_up(self) -> None:
#         algoscene.reset_mock()
#         self.test_list2 = [1, 2, 4]
#         self.algolist = AlgoList(algoscene, test_list)
#         self.algolist2 = AlgoList(algoscene, self.test_list2)
#         self.expected_list = test_list + self.test_list2
#
#         # Sort the expected list
#         self.expected_list.sort()

    # Check that the internal representation is represented accordingly
    def test_merge_internal_list_sorted_and_contains_all(self):
        algoscene.reset_mock()
        test_list2 = [1, 2, 4]
        algolist = AlgoList(algoscene, test_list)
        algolist2 = AlgoList(algoscene, test_list2)
        expected_list = test_list + test_list2

        # Sort the expected list
        expected_list.sort()

        merged_list = algolist.merge(algolist, algolist2)

        assert expected_list == [n.val for n in merged_list.nodes]

    # Check that a few key solutions were called
    @patch("algomanim.algolist.AlgoList.replace")
    @patch("algomanim.algolist.AlgoList.hide_list")
    def test_key_merge_internal_calls(self, hide_list, replace):
        algoscene.reset_mock()
        test_list2 = [1, 2, 4]
        algolist = AlgoList(algoscene, test_list)
        algolist2 = AlgoList(algoscene, test_list2)

        _ = algolist.merge(algolist, algolist2)
        assert hide_list.call_count == 3

        _ = algolist.merge(algolist, algolist2, replace=True)
        replace.assert_called_once()

# --------------- Concat Tests --------------- #
#     def concat_set_up(self) -> None:
#         self.algoscene.reset_mock()
#         self.test_list2 = [1, 2, 4]
#         self.algolist = AlgoList(algoscene, test_list)
#         self.algolist2 = AlgoList(algoscene, self.test_list2)
#         self.expected_list = test_list + self.test_list2

    # Check that the internal representation is represented accordingly
    def test_concat_internal_list_contains_all(self):
        algoscene.reset_mock()
        test_list2 = [1, 2, 4]
        algolist = AlgoList(algoscene, test_list)
        algolist2 = AlgoList(algoscene, test_list2)
        expected_list = test_list + test_list2

        concat_list = algolist.concat(algolist2)

        assert expected_list == [n.val for n in concat_list.nodes]

    # # Check that a few key solutions were called
    # @patch("algomanim.algolist.AlgoList.center")
    # @patch("algomanim.algolist.AlgoList.group")
    # def test_key_concat_internal_calls(self, group, center):
    #     self.concat_set_up()
    #
    #     x = self.algolist.concat(self.algolist2)
    #     group.assert_called_once()
    #
    #     y = self.algolist.concat(self.algolist2, center=True)
    #     center.assert_called_once()
