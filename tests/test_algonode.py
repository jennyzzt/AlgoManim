# pylint: disable=R0201
from unittest.mock import patch, Mock
from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algonode import AlgoNode


algoscene = AlgoScene()
DEFAULT_VAL = 5


@patch("algomanim.algonode.VGroup", Mock())
@patch('algomanim.algoscene.TextMobject', Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
class TestAlgoNode:

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_change_value_adds_action_pair(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        assert algonode.val == DEFAULT_VAL
        old_text = algonode.txt
        old_num_action_pairs = len(algoscene.action_pairs)

        new_val = 6
        algonode.change_value(new_val)

        assert algonode.val == new_val
        create_static_action.assert_called_once_with(
            algonode.static_replace_text, [old_text, algonode.txt]
        )
        assert len(algoscene.action_pairs) == old_num_action_pairs + 1

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_highlight_adds_action_pair(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        old_num_action_pairs = len(algoscene.action_pairs)

        algonode.highlight()

        create_static_action.assert_called_once_with(
            algonode.node.set_fill,
            [algonode.highlight_color],
            color_index=0
        )
        assert len(algoscene.action_pairs) == old_num_action_pairs + 1

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_dehighlight_adds_action_pair(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        old_num_action_pairs = len(algoscene.action_pairs)

        algonode.dehighlight()

        create_static_action.assert_called_once_with(
            algonode.node.set_fill,
            [algonode.node_color],
            color_index=0
        )
        assert len(algoscene.action_pairs) == old_num_action_pairs + 1

    def test_add_line_adds_two_action_pairs(self):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        targetnode = AlgoNode(algoscene, DEFAULT_VAL)
        old_num_action_pairs = len(algoscene.action_pairs)

        algonode.add_line(targetnode)

        assert targetnode.lines[algonode] == algonode.lines[targetnode]
        assert len(algoscene.action_pairs) == old_num_action_pairs + 2

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_highlight_line_existing_adds_action_pair(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        targetnode = AlgoNode(algoscene, DEFAULT_VAL)
        algonode.add_line(targetnode)
        old_num_action_pairs = len(algoscene.action_pairs)
        create_static_action.reset_mock()

        algonode.highlight_line(targetnode)

        create_static_action.assert_called_once_with(
            algonode.lines[targetnode].set_color,
            [algonode.highlight_color],
            color_index=0
        )
        assert len(algoscene.action_pairs) == old_num_action_pairs + 1

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_highlight_line_not_existing_does_nothing(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        targetnode = AlgoNode(algoscene, DEFAULT_VAL)
        create_static_action.reset_mock()

        algonode.highlight_line(targetnode)

        create_static_action.assert_not_called()

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_dehighlight_line_existing_adds_action_pair(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        targetnode = AlgoNode(algoscene, DEFAULT_VAL)
        algonode.add_line(targetnode)
        old_num_action_pairs = len(algoscene.action_pairs)
        create_static_action.reset_mock()

        algonode.dehighlight_line(targetnode)

        create_static_action.assert_called_once_with(
            algonode.lines[targetnode].set_color,
            [WHITE],
            color_index=0
        )
        assert len(algoscene.action_pairs) == old_num_action_pairs + 1

    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_dehighlight_line_not_existing_does_nothing(self, create_static_action):
        algonode = AlgoNode(algoscene, DEFAULT_VAL)
        targetnode = AlgoNode(algoscene, DEFAULT_VAL)
        create_static_action.reset_mock()

        algonode.dehighlight_line(targetnode)

        create_static_action.assert_not_called()
