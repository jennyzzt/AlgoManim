# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algoscene import AlgoScene, AlgoTransform


mock_animation = Mock()

@patch("algomanim.algoscene.Scene.play")
class TestAlgoScene:
    def test_constructor_plays_queued_animations(self, play):
        AlgoSceneTestSingle()
        play.assert_called_once_with(mock_animation)


    def test_w_prev_combines_animations(self, play):
        AlgoSceneTestDoubleTogether()
        play.assert_called_once_with(mock_animation, mock_animation)
        play.reset_mock()

        AlgoSceneTestDoubleNotTogether()
        assert play.call_count == 2


# AlgoScene instantiations with specific algoconstructs for test cases
class AlgoSceneTestSingle(AlgoScene):
    def algoconstruct(self):
        self.add_action(self.play, AlgoTransform([mock_animation]))


class AlgoSceneTestDoubleTogether(AlgoScene):
    def algoconstruct(self):
        self.add_action(self.play, AlgoTransform([mock_animation]))
        self.add_action(self.play, AlgoTransform([mock_animation]), w_prev=True)


class AlgoSceneTestDoubleNotTogether(AlgoScene):
    def algoconstruct(self):
        self.add_action(self.play, AlgoTransform([mock_animation]))
        self.add_action(self.play, AlgoTransform([mock_animation]), w_prev=False)
