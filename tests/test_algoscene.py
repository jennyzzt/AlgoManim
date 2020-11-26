# pylint: disable=R0201, R0913, R0904
from unittest.mock import patch, Mock
from manimlib.imports import *
from algomanim.algoaction import AlgoTransform
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from algomanim.settings import DEFAULT_SETTINGS


mock_action_pair = Mock()
mock_static = Mock()
mock_animation = Mock()
mock_transform = Mock()
mock_node = Mock()
mock_customisation = Mock()

mock_color = Mock()


@patch('algomanim.algolist.VGroup', Mock())
@patch('algomanim.algonode.VGroup', Mock())
@patch('algomanim.algoobject.TexMobject', Mock())
@patch('algomanim.algoscene.TextMobject', Mock())
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

    def test_shift_scene_calls_set_next_to_on_all_objs(self):
        algoscene = AlgoScene()
        num_objs = 5
        for _ in range(num_objs):
            algoscene.algo_objs.append(mock_node)

        algoscene.shift_scene(UP)

        assert mock_node.set_next_to.call_count == num_objs

    def test_skip_without_end_skips_all_action_pairs_from_start(self):
        algoscene = AlgoScene()
        num_action_pairs = 5
        algoscene.action_pairs = [mock_animation for _ in range(num_action_pairs)]
        mock_animation.reset_mock()

        start = 1
        algoscene.skip(start)

        assert mock_animation.skip.call_count == num_action_pairs - start

    def test_skip_with_end_skips_all_action_pairs_in_range(self):
        algoscene = AlgoScene()
        num_action_pairs = 5
        algoscene.action_pairs = [mock_animation for _ in range(num_action_pairs)]
        mock_animation.reset_mock()

        start = 1
        end = 3
        algoscene.skip(start, end=end)

        assert mock_animation.skip.call_count == end - start

    def test_fast_forward_without_end_ffs_all_action_pairs_from_start(self):
        algoscene = AlgoScene()
        num_action_pairs = 5
        algoscene.action_pairs = [mock_animation for _ in range(num_action_pairs)]
        mock_animation.reset_mock()

        start = 1
        algoscene.fast_forward(start)

        assert mock_animation.fast_forward.call_count == num_action_pairs - start

    def test_fast_forward_with_end_ffs_all_action_pairs_in_range(self):
        algoscene = AlgoScene()
        num_action_pairs = 5
        algoscene.action_pairs = [mock_animation for _ in range(num_action_pairs)]
        mock_animation.reset_mock()

        start = 1
        end = 3
        algoscene.fast_forward(start, end=end)

        assert mock_animation.fast_forward.call_count == end - start

    @patch('algomanim.algoscene.AlgoScene.add_fade_in_all')
    @patch('algomanim.algoscene.AlgoScene.remove_text')
    @patch('algomanim.algoscene.AlgoScene.add_wait')
    @patch('algomanim.algoscene.AlgoScene.add_text')
    @patch('algomanim.algoscene.AlgoScene.add_fade_out_all')
    def test_add_slide_calls_a_sequence_of_animations(self, add_fade_out_all, add_text,
                                                      add_wait, remove_text, add_fade_in_all):
        algoscene = AlgoScene()

        slide_text = 'new slide!'
        index = 0
        algoscene.add_slide(slide_text, index)

        add_fade_out_all.assert_called_once_with(index)
        add_text.assert_called_once_with(slide_text, index+1, position=ORIGIN)
        add_wait.assert_called_once_with(index + 2, wait_time=1)
        remove_text.assert_called_once()
        add_fade_in_all.assert_called_once_with(index + 4)

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    def test_add_fade_out_all_inserts_action_pair_and_metadata(self, insert_action_pair,
                                                               add_metadata):
        algoscene = AlgoScene()

        algoscene.add_fade_out_all(0)

        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    def test_add_fade_in_all_inserts_action_pair_and_metadata(self, insert_action_pair,
                                                               add_metadata):
        algoscene = AlgoScene()

        algoscene.add_fade_in_all(0)

        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    def test_add_wait_inserts_action_pair_and_metadata(self, insert_action_pair,
                                                       add_metadata):
        algoscene = AlgoScene()

        algoscene.add_wait(0)

        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_add_clear_inserts_action_pair_and_metadata(self, create_static_action,
                                                        insert_action_pair,
                                                        add_metadata):
        algoscene = AlgoScene()

        algoscene.add_clear(0)

        create_static_action.assert_called_once_with(algoscene.clear)
        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    def test_track_algoitem_appends_to_algo_objs(self):
        algoscene = AlgoScene()
        old_num_algoobjs = len(algoscene.algo_objs)

        algoscene.track_algoitem(mock_node)

        assert len(algoscene.algo_objs) == old_num_algoobjs + 1
        assert mock_node in algoscene.algo_objs

    def test_untrack_algoitem_existing_removes_from_algo_objs(self):
        algoscene = AlgoScene()
        algoscene.track_algoitem(mock_node)
        old_num_algoobjs = len(algoscene.algo_objs)

        algoscene.untrack_algoitem(mock_node)

        assert len(algoscene.algo_objs) == old_num_algoobjs - 1
        assert mock_node not in algoscene.algo_objs

    def test_create_play_action_creates_play_action(self):
        algoscene = AlgoScene()
        action = algoscene.create_play_action(mock_transform)
        assert action.act == algoscene.play
        assert action.transform == mock_transform

    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    def test_add_action_pair_creates_pair_and_inserts_it(self, insert_action_pair):
        algoscene = AlgoScene()
        index = 0
        pair = algoscene.add_action_pair(mock_animation, index=index)

        assert pair.anim_action == mock_animation
        assert pair.static_action == mock_animation
        insert_action_pair.assert_called_once_with(pair, index)

    @patch('algomanim.algoaction.AlgoSceneActionPair.attach_index')
    def test_insert_action_pair_adds_to_back_if_index_not_given(self, attach_index):
        algoscene = AlgoScene()
        initial_size = 3
        for _ in range(initial_size):
            algoscene.add_action_pair(mock_action_pair)
        attach_index.reset_mock()

        algoscene.add_action_pair(mock_action_pair)

        attach_index.assert_called_once_with(initial_size)
        assert len(algoscene.action_pairs) == initial_size + 1

    @patch('algomanim.algoaction.AlgoSceneActionPair.attach_index')
    @patch('algomanim.algoscene.AlgoScene.push_back_action_pair_indices')
    def test_insert_action_pair_adds_to_given_index(self, push_back_action_pair_indices,
                                                    attach_index):
        algoscene = AlgoScene()
        initial_size = 3
        for _ in range(initial_size):
            algoscene.add_action_pair(mock_action_pair)
        attach_index.reset_mock()

        index = 1
        algoscene.add_action_pair(mock_action_pair, index=index)

        push_back_action_pair_indices.assert_called_once_with(index)
        attach_index.assert_called_once_with(index)
        assert len(algoscene.action_pairs) == initial_size + 1

    @patch('algomanim.algoscene.AlgoScene.add_metadata')
    @patch('algomanim.algoscene.AlgoScene.insert_action_pair')
    @patch('algomanim.algoaction.AlgoSceneAction.create_static_action')
    def test_add_static_inserts_action_pair_and_metadata(self, create_static_action,
                                                         insert_action_pair, add_metadata):
        algoscene = AlgoScene()

        algoscene.add_static(0, mock_static)

        create_static_action.assert_called_once_with(mock_static, [])
        insert_action_pair.assert_called_once()
        add_metadata.assert_called_once()

    # ---------- test algoscene pipeline structure ----------

    @patch('algomanim.animation_block.AnimationBlock.run')
    @patch('algomanim.algoaction.AlgoSceneActionPair.attach_index')
    @patch('algomanim.algoscene.AlgoScene.add_wait')
    def test_execute_action_pairs_process_and_run_action_pairs(self, add_wait, attach_index, run):
        algoscene = AlgoScene()
        size = 3
        for _ in range(size):
            algoscene.add_action_pair(mock_action_pair)
            algoscene.post_customize_fns.append(mock_customisation)
        attach_index.reset_mock()

        algoscene.execute_action_pairs(algoscene.action_pairs, algoscene.anim_blocks)

        # test that wait is added at the end
        add_wait.assert_called_once_with(size)
        # test that indexes are attached
        assert attach_index.call_count == size
        # test that post customisations are added
        assert mock_customisation.call_count == size
        # test that animations are run
        assert run.call_count == len(algoscene.anim_blocks)

    @patch('algomanim.algoscene.AlgoScene.create_metadata_blocks')
    @patch('algomanim.algoscene.AlgoScene.execute_action_pairs')
    @patch('algomanim.algoscene.AlgoScene.customize_construct')
    @patch('algomanim.algoscene.AlgoScene.algo_construct')
    @patch('algomanim.algoscene.AlgoScene.post_config')
    @patch('algomanim.algoscene.AlgoScene.preconfig')
    def test_construct_pipeline(self, preconfig, post_config,
                                algo_construct, customize_construct,
                                execute_action_pairs,
                                create_metadata_blocks):
        algoscene = AlgoScene()
        preconfig.reset_mock()
        post_config.reset_mock()
        algo_construct.reset_mock()
        customize_construct.reset_mock()
        execute_action_pairs.reset_mock()
        create_metadata_blocks.reset_mock()

        algoscene.construct()

        preconfig.assert_called_once_with(algoscene.settings)
        post_config.assert_called_once_with(algoscene.settings)

        algo_construct.assert_called_once_with()
        customize_construct.assert_called_once_with()

        execute_action_pairs.assert_called_once_with(algoscene.action_pairs, algoscene.anim_blocks)
        create_metadata_blocks.assert_called_once_with()

    @patch('algomanim.algoscene.Scene.play')
    def test_constructor_plays_queued_animations(self, play):
        AlgoSceneTestSingle()
        play.assert_called_once_with(mock_animation())

    @patch('algomanim.algoscene.Scene.play')
    def test_w_prev_combines_animations(self, play):
        AlgoSceneTestDoubleTogether()
        play.assert_called_once_with(mock_animation(), mock_animation())
        play.reset_mock()

        AlgoSceneTestDoubleNotTogether()
        assert play.call_count == 2

    @patch('algomanim.algoscene.Scene.play')
    def test_set_color(self, play):
        AlgoSceneCustomColor()
        play.assert_called_once_with(mock_animation(mock_color))


@patch('algomanim.algonode.VGroup', Mock())
@patch('algomanim.algoscene.TextMobject', Mock())
@patch('algomanim.algoobject.TexMobject', Mock())
class TestAlgoScenePreconfig:
    @patch('algomanim.algonode.Square')
    def test_change_node_color(self, square):
        algoscene = AlgoSceneNodeColorHex()
        square.assert_any_call(
            fill_color=algoscene.test_color,
            fill_opacity=1,
            side_length=DEFAULT_SETTINGS['node_size']
        )

    @patch('algomanim.algonode.Circle')
    def test_change_node_shape(self, circle):
        AlgoSceneNodeCircle()
        circle.assert_any_call(
            color=DEFAULT_SETTINGS['node_color'],
            fill_opacity=1,
            radius=DEFAULT_SETTINGS['node_size'] / 2
        )

    @patch('algomanim.algoscene.Text')
    def test_change_node_font(self, text):
        scene = AlgoSceneNodeFont()
        text.assert_any_call(
            str(scene.test_list[0]),
            color=scene.test_font_color,
            font=scene.test_font
        )

    @patch('algomanim.algoscene.AlgoScene.execute_action_pairs', Mock())
    @patch('algomanim.algoscene.AlgoScene.create_metadata_blocks', Mock())
    @patch('algomanim.algoscene.Text')
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

class AlgoSceneMockList(AlgoScene):
    test_list = [1]

    @patch('algomanim.algoscene.TexMobject', Mock())
    @patch('algomanim.algolist.AlgoList.group', Mock())
    @patch('algomanim.algolist.AlgoList.center', Mock())
    @patch('algomanim.algolist.AlgoList.show_list', Mock())
    def algo(self):
        AlgoList(self, self.test_list)

class AlgoSceneNodeColorHex(AlgoSceneMockList):
    test_color = '#FFFF00'

    def preconfig(self, settings):
        settings['node_color'] = self.test_color

class AlgoSceneNodeCircle(AlgoSceneMockList):
    def preconfig(self, settings):
        settings['node_shape'] = 'circle'

class AlgoSceneNodeFont(AlgoSceneMockList):
    test_font = 'sans-serif'
    test_font_color = '#FFFF00'

    def preconfig(self, settings):
        settings['node_font'] = self.test_font
        settings['node_font_color'] = self.test_font_color

class AlgoSceneTextFont(AlgoSceneMockList):
    test_text = 'Test'
    test_font = 'sans-serif'
    test_font_color = '#FFFF00'

    def preconfig(self, settings):
        settings['text_font'] = self.test_font
        settings['text_font_color'] = self.test_font_color

    def customize(self):
        self.add_text(self.test_text)
