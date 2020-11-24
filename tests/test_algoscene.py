# pylint: disable=R0201
from unittest.mock import patch, Mock
from manimlib.imports import *
from algomanim.algoaction import AlgoTransform, AlgoSceneAction
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.settings import DEFAULT_SETTINGS


mock_animation = Mock()
mock_color = Mock()
mock_node = Mock()


@patch("algomanim.algolist.VGroup", Mock())
@patch("algomanim.algonode.VGroup", Mock())
@patch("algomanim.algoobject.TexMobject", Mock())
@patch("algomanim.algoscene.TextMobject", Mock())
class TestAlgoScene:

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    def test_add_transform_adds_action_pair_and_metadata(self, insert_action_pair, add_metadata):
        algoscene = AlgoScene()
        algoscene.add_transform(0)
        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    @patch('algomanim.algoaction.AlgoSceneAction.create_empty_action')
    def test_insert_pin_adds_empty_action_pair_and_metadata(self,
                                                            create_empty_action,
                                                            insert_action_pair,
                                                            add_metadata):
        algoscene = AlgoScene()
        algoscene.insert_pin('test')
        create_empty_action.assert_called_once()
        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.find_action_pairs')
    def test_find_pin_calls_find_action_pairs(self, find_action_pairs):
        algoscene = AlgoScene()
        algoscene.insert_pin('test')
        find_action_pairs.reset_mock()
        algoscene.find_pin('test')
        find_action_pairs.assert_called_once()

    def test_find_action_pairs_returns_action_pairs_with_metadata_name(self):
        algoscene = AlgoScene()
        algoscene.insert_pin('nottest')
        num_test_metas = 3
        for _ in range(num_test_metas):
            algoscene.insert_pin('test')

        action_pairs = algoscene.find_action_pairs('test')

        assert len(action_pairs) == num_test_metas

    @patch('algomanim.algoscene.AlgoScene.add_transform')
    def test_chain_pin_highlight_no_args_does_nothing(self, add_transform):
        algoscene = AlgoScene()
        num_test_metas = 3
        for _ in range(num_test_metas):
            algoscene.insert_pin('test')

        algoscene.chain_pin_highlight('test')

        add_transform.assert_not_called()

    @patch('algomanim.algoscene.AlgoScene.add_transform')
    def test_chain_pin_highlight_with_args_adds_transforms(self, add_transform):
        algoscene = AlgoScene()
        num_test_metas = 3
        for _ in range(num_test_metas):
            algoscene.insert_pin('test', mock_node)
        add_transform.reset_mock()

        algoscene.chain_pin_highlight('test')

        assert add_transform.call_count == num_test_metas * 2 - 1

    @patch('algomanim.algoscene.AlgoScene.add_transform')
    @patch('algomanim.algoscene.AlgoScene.create_text')
    def test_add_text_creates_text_and_adds_transform(self, create_text, add_transform):
        algoscene = AlgoScene()
        test_text = 'test'
        algoscene.add_text(test_text)

        create_text.assert_called_once_with(test_text)
        add_transform.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_transform')
    @patch('algomanim.algoscene.AlgoScene.create_text')
    def test_change_text_with_oldobj_creates_new_text_and_adds_transform(self, create_text,
                                                                         add_transform):
        algoscene = AlgoScene()
        test_text = 'test'
        old_textobj = algoscene.add_text(test_text)
        create_text.reset_mock()
        add_transform.reset_mock()

        new_test_text = 'new test'
        algoscene.change_text(new_test_text, old_textobj)

        create_text.assert_called_once_with(new_test_text)
        add_transform.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_text')
    def test_change_text_without_oldobj_adds_text(self, add_text):
        algoscene = AlgoScene()
        test_text = 'test'
        algoscene.add_text(test_text)
        add_text.reset_mock()

        new_test_text = 'new test'
        index = 0
        algoscene.change_text(new_test_text, index=index)

        add_text.assert_called_once_with(new_test_text, index=index, position=ORIGIN)

    @patch('algomanim.algoscene.AlgoScene.add_transform')
    def test_remove_text_adds_transform(self, add_transform):
        algoscene = AlgoScene()
        test_text = 'test'
        old_textobj = algoscene.add_text(test_text)
        add_transform.reset_mock()

        algoscene.remove_text(old_textobj)

        add_transform.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.change_text')
    def test_add_complexity_analysis_line_does_nothing_if_not_show_code(self, change_text):
        algoscene = AlgoSceneMockList()
        change_text.reset_mock()
        algoscene.add_complexity_analysis_line(1)
        change_text.assert_not_called()

    @patch('algomanim.algoscene.AlgoScene.change_text')
    def test_add_complexity_analysis_line_calls_change_text(self, change_text):
        algoscene = AlgoScene()
        line_num = 1
        line_call_times = 3
        for _ in range(line_call_times):
            algoscene.insert_pin('__codeindex__', line_num)
        change_text.reset_mock()

        algoscene.add_complexity_analysis_line(line_num)

        assert change_text.call_count == line_call_times

    @patch('algomanim.algoscene.AlgoScene.change_text')
    def test_add_complexity_analysis_fn_calls_change_text(self, change_text):
        algoscene = AlgoScene()
        fn_name = 'foo'
        fn_call_times = 3
        for _ in range(fn_call_times):
            algoscene.insert_pin(fn_name)
        change_text.reset_mock()

        algoscene.add_complexity_analysis_fn(fn_name)

        assert change_text.call_count == fn_call_times

        

        

    @patch("algomanim.algoscene.Scene.play")
    def test_constructor_plays_queued_animations(self, play):
        AlgoSceneTestSingle()
        play.assert_called_once_with(mock_animation())

    @patch("algomanim.algoscene.Scene.play")
    def test_w_prev_combines_animations(self, play):
        AlgoSceneTestDoubleTogether()
        play.assert_called_once_with(mock_animation(), mock_animation())
        play.reset_mock()

        AlgoSceneTestDoubleNotTogether()
        assert play.call_count == 2

    @patch("algomanim.algoscene.Scene.play")
    def test_set_color(self, play):
        AlgoSceneCustomColor()
        play.assert_called_once_with(mock_animation(mock_color))

    @patch("algomanim.algoscene.Scene.play")
    def test_fast_forward(self, play):
        AlgoSceneFastForward()
        # Original speed is 1s, fast forward halves it
        play.assert_called_once_with(mock_animation(), run_time=0.5)

    @patch("algomanim.algoscene.Scene.play")
    @patch("algomanim.algoscene.Scene.add")
    def test_skip(self, add, play):
        AlgoSceneSkip()
        play.assert_not_called()
        add.assert_called_once_with(mock_animation())

    @patch("algomanim.algoscene.Scene.wait")
    def test_wait(self, wait):
        AlgoSceneWait()
        assert wait.call_count == 2

    @patch("algomanim.algoscene.Scene.play")
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

    def customize(self, action_pairs):
        action_pairs[0].set_color(mock_color)


class AlgoSceneFastForward(AlgoScene):
    def algo(self):
        action = self.create_play_action(default_transform)
        self.add_action_pair(action, action)

    def customize(self, action_pairs):
        self.fast_forward(0)


class AlgoSceneSkip(AlgoScene):
    def algo(self):
        self.add_action_pair(
            AlgoSceneAction(self.play, default_transform),
            AlgoSceneAction(self.add, default_transform)
        )

    def customize(self, action_pairs):
        self.skip(0)


class AlgoSceneWait(AlgoScene):
    def customize(self, action_pairs):
        self.add_wait(0)


class AlgoSceneClear(AlgoScene):
    def customize(self, action_pairs):
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

    def customize(self, action_pairs):
        self.add_text(self.test_text)
