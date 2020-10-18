# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algoscene import AlgoScene, AlgoTransform, AlgoSceneAction


mock_animation = Mock()

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


# AlgoScene instantiations with specific algoconstructs for test cases
class AlgoSceneTestSingle(AlgoScene):
    def algoconstruct(self):
        action = AlgoSceneAction(self.play, AlgoTransform([], transform=mock_animation))
        anim_action = action
        self.add_action_pair(anim_action, action)

class AlgoSceneTestDoubleTogether(AlgoScene):
    def algoconstruct(self):
        anim_action = AlgoSceneAction(self.play, AlgoTransform([], transform=mock_animation))
        action = anim_action
        self.add_action_pair(anim_action, action)

        anim_action = AlgoSceneAction(self.play, AlgoTransform([], transform=mock_animation),
            w_prev=True)
        action = anim_action
        self.add_action_pair(anim_action, action)


class AlgoSceneTestDoubleNotTogether(AlgoScene):
    def algoconstruct(self):
        anim_action = AlgoSceneAction(self.play, AlgoTransform([], transform=mock_animation))
        action = anim_action
        self.add_action_pair(anim_action, action)

        anim_action = AlgoSceneAction(self.play, AlgoTransform([], transform=mock_animation))
        action = anim_action
        self.add_action_pair(anim_action, action)
