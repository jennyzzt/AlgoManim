# pylint: disable=R0201
from unittest.mock import patch, Mock
from algomanim.algoaction import AlgoTransform, AlgoSceneAction
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.settings import DEFAULT_SETTINGS


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


    def test_set_color(self, play):
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

    @patch("algomanim.algoscene.Scene.clear")
    def test_clear(self, clear, _):
        AlgoSceneClear()
        clear.assert_called_once_with()


@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algoscene.TextMobject", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
class TestAlgoScenePreconfig:
    @patch("algomanim.algonode.Square")
    def test_change_node_color(self, square):
        algoscene = AlgoSceneNodeColorHex()
        square.assert_any_call(
            fill_color=algoscene.test_color,
            fill_opacity=1,
            side_length=DEFAULT_SETTINGS['node_size']
        )

    @patch("algomanim.algonode.Circle")
    def test_change_node_shape(self, circle):
        AlgoSceneNodeCircle()
        circle.assert_any_call(
            color=DEFAULT_SETTINGS['node_color'],
            fill_opacity=1,
            radius=DEFAULT_SETTINGS['node_size'] / 2
        )

    @patch("algomanim.algoscene.Text")
    def test_change_node_font(self, text):
        scene = AlgoSceneNodeFont()
        text.assert_any_call(
            str(scene.test_list[0]),
            color=scene.test_font_color,
            font=scene.test_font
        )

    @patch("algomanim.algoscene.AlgoScene.execute_action_pairs", Mock())
    @patch("algomanim.algoscene.AlgoScene.create_metadata_blocks", Mock())
    @patch("algomanim.algoscene.Text")
    def test_change_text_font(self, text):
        scene = AlgoSceneTextFont()
        text.assert_any_call(
            scene.test_text,
            color=scene.test_font_color,
            font=scene.test_font
        )


# AlgoScene instantiations with specific algoconstructs for test cases
default_transform = AlgoTransform([], transform=mock_animation)

class AlgoSceneTestSingle(AlgoScene):
    def algo(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)


class AlgoSceneTestDoubleTogether(AlgoScene):
    def algo(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)
        action = self.create_play_action(default_transform, w_prev=True)
        self.add_action_pair(action, action)


class AlgoSceneTestDoubleNotTogether(AlgoScene):
    def algo(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)
        self.add_action_pair(action, action)


class AlgoSceneCustomColor(AlgoScene):
    def algo(self):
        original_color = Mock()
        action = self.create_play_action(
            AlgoTransform([original_color], transform=mock_animation, color_index=0)
        )
        self.add_action_pair(action, action)

    def customize(self):
        self.action_pairs[0].set_color(mock_color)


class AlgoSceneFastForward(AlgoScene):
    def algo(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)

    def customize(self):
        self.fast_forward(0)


class AlgoSceneSkip(AlgoScene):
    def algo(self):
        self.add_action_pair(
            AlgoSceneAction(self.play, default_transform),
            AlgoSceneAction(self.add, default_transform)
        )

    def customize(self):
        self.skip(0)


class AlgoSceneWait(AlgoScene):
    def customize(self):
        self.add_wait(0)


class AlgoSceneClear(AlgoScene):
    def customize(self):
        self.clear()


class AlgoSceneMockList(AlgoScene):
    test_list = [1]

    @patch("algomanim.algoscene.TexMobject", Mock())
    @patch("algomanim.algolist.AlgoList.group", Mock())
    @patch("algomanim.algolist.AlgoList.center", Mock())
    @patch("algomanim.algolist.AlgoList.show_list", Mock())
    def algo(self):
        AlgoList(self, self.test_list)


class AlgoSceneNodeColorHex(AlgoSceneMockList):
    test_color = "#FFFF00"

    def preconfig(self, settings):
        settings['node_color'] = self.test_color


class AlgoSceneNodeCircle(AlgoSceneMockList):
    def preconfig(self, settings):
        settings['node_shape'] = 'circle'


class AlgoSceneNodeFont(AlgoSceneMockList):
    test_font = 'sans-serif'
    test_font_color = "#FFFF00"

    def preconfig(self, settings):
        settings['node_font'] = self.test_font
        settings['node_font_color'] = self.test_font_color


class AlgoSceneTextFont(AlgoSceneMockList):
    test_text = 'Test'
    test_font = 'sans-serif'
    test_font_color = "#FFFF00"

    def preconfig(self, settings):
        settings['text_font'] = self.test_font
        settings['text_font_color'] = self.test_font_color

    def customize(self):
        self.add_text(self.test_text)
