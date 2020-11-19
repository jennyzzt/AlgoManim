#pylint: disable=R0201
from unittest.mock import patch, Mock
from manimlib.imports import *
from algomanim.algoobject import AlgoObject


algoscene = Mock()
other_algo_object = Mock()


@patch('algomanim.algoscene.TextMobject', Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
@patch.object(AlgoObject, '__abstractmethods__', set())
class TestAlgoObject:

    def test_set_next_to_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.set_next_to(other_algo_object, RIGHT)
        algoscene.add_action_pair.assert_called_once()

    def test_set_relative_to_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.set_relative_to(other_algo_object, RIGHT)
        algoscene.add_action_pair.assert_called_once()

    def test_swap_with_adds_two_action_pairs(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.swap_with(other_algo_object)
        assert algoscene.add_action_pair.call_count == 2

    def test_center_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.center()
        algoscene.add_action_pair.assert_called_once()

    def test_show_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.show()
        algoscene.add_action_pair.assert_called_once()

    def test_hide_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.hide()
        algoscene.add_action_pair.assert_called_once()

    def test_hide_group_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.hide_group(other_algo_object)
        algoscene.add_action_pair.assert_called_once()

    def test_add_text_without_key_adds_two_action_pairs(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.add_text('test', 'key')
        assert algoscene.add_action_pair.call_count == 2

    def test_add_text_with_existing_key_adds_three_action_pairs(self):
        algo_object = DummyAlgoObject(algoscene)
        algo_object.add_text('test', 'key')
        algoscene.reset_mock()
        algo_object.add_text('test', 'key')
        assert algoscene.add_action_pair.call_count == 3

    def test_remove_text_without_key_removes_all_text(self):
        algo_object = DummyAlgoObject(algoscene)
        num_texts = 2
        for i in range(num_texts):
            algo_object.add_text(f'test{i}', f'key{i}')
        algoscene.reset_mock()
        algo_object.remove_text()
        assert algoscene.add_action_pair.call_count == num_texts+1

    def test_remove_text_with_exising_key_removes_only_that_text(self):
        algo_object = DummyAlgoObject(algoscene)
        num_texts = 2
        for i in range(num_texts):
            algo_object.add_text(f'test{i}', f'key{i}')
        algoscene.reset_mock()
        algo_object.remove_text(key='key0')
        algoscene.add_action_pair.assert_called_once()

    def test_move_group_to_group_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        AlgoObject.move_group_to_group(algoscene, algo_object.grp, other_algo_object.grp)
        algoscene.add_action_pair.assert_called_once()

    def test_move_to_calculated_pt_adds_action_pair(self):
        algo_object = DummyAlgoObject(algoscene)
        algoscene.reset_mock()
        algo_object.move_to_calculated_pt([other_algo_object], pt_fn=AlgoObject.center_pt)
        algoscene.add_action_pair.assert_called_once()


class DummyAlgoObject(AlgoObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.grp = VGroup()
