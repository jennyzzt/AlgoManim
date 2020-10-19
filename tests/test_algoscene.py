# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algoscene import AlgoScene, AlgoTransform, AlgoSceneAction


mock_animation = Mock()
mock_color = Mock()

@patch("algomanim.algoscene.Scene.play")
class TestAlgoScene:
    def test_constructor_plays_queued_animations(self, play):
        AlgoSceneTestSingle()
        play.assert_called_once_with(mock_animation())


    def test_w_prev_combines_animations(self, play):
        AlgoSceneTestDoubleTogether()
        play.assert_called_once_with(mock_animation(), mock_animation())
        play.reset_mock()

        AlgoSceneTestDoubleNotTogether()
        assert play.call_count == 2


    def test_change_color(self, play):
        AlgoSceneCustomColor()
        play.assert_called_once_with(mock_animation(mock_color))


    def test_fast_forward(self, play):
        AlgoSceneFastForward()
        # Original speed is 1s, fast forward halves it
        play.assert_called_once_with(mock_animation(), run_time=0.5)


    @patch("algomanim.algoscene.Scene.add")
    def test_skip(self, add, play):
        AlgoSceneSkip()
        play.assert_not_called()
        add.assert_called_once_with(mock_animation())


    @patch("algomanim.algoscene.Scene.wait")
    def test_wait(self, wait, _):
        AlgoSceneWait()
        assert wait.call_count == 2


default_transform = AlgoTransform([], transform=mock_animation)

# AlgoScene instantiations with specific algoconstructs for test cases
class AlgoSceneTestSingle(AlgoScene):
    def algoconstruct(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)


class AlgoSceneTestDoubleTogether(AlgoScene):
    def algoconstruct(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)
        action = self.create_play_action(default_transform, w_prev=True)
        self.add_action_pair(action, action)


class AlgoSceneTestDoubleNotTogether(AlgoScene):
    def algoconstruct(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)
        self.add_action_pair(action, action)


class AlgoSceneCustomColor(AlgoScene):
    def algoconstruct(self):
        original_color = Mock()
        action = self.create_play_action(
            AlgoTransform([original_color], transform=mock_animation, color_index=0)
        )
        self.add_action_pair(action, action)

    def customize(self, action_pairs):
        action_pairs[0].change_color(mock_color)


class AlgoSceneFastForward(AlgoScene):
    def algoconstruct(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)

    def customize(self, action_pairs):
        self.fast_forward(0)


class AlgoSceneSkip(AlgoScene):
    def algoconstruct(self):
        self.add_action_pair(
            AlgoSceneAction(self.play, default_transform),
            AlgoSceneAction(self.add, default_transform)
        )

    def customize(self, action_pairs):
        self.skip(0)


class AlgoSceneWait(AlgoScene):
    def customize(self, action_pairs):
        self.add_wait(0)
