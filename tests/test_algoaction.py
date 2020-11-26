# pylint: disable=R0201, R0903, W0143
from unittest.mock import Mock
from algomanim.algoaction import AlgoSceneActionPair, AlgoSceneAction, AlgoTransform, do_nothing


mock_anim = Mock()
mock_static = Mock()
mock_fn = Mock()
mock_args = Mock()
mock_index = Mock()


class TestAlgoSceneActionPair:

    def test_set_runtime_does_nothing_if_no_runtime(self):
        actionpair = AlgoSceneActionPair(mock_anim)
        actionpair.set_runtime(0)
        assert actionpair.run_time is None

    def test_set_runtime_cannot_skip_non_anim_action(self):
        run_time = 1
        actionpair = AlgoSceneActionPair(mock_anim, run_time=run_time)
        actionpair.set_runtime(0)
        assert actionpair.run_time == run_time

    def test_set_runtime_changes_runtime(self):
        actionpair = AlgoSceneActionPair(mock_anim, static_action=mock_static, run_time=1)
        new_run_time = 2
        actionpair.set_runtime(new_run_time)
        assert actionpair.run_time == new_run_time

class TestAlgoSceneAction:

    def test_create_static_action_returns_algosceneaction(self):
        sceneaction = AlgoSceneAction.create_static_action(mock_fn, args=mock_args,
                                                           color_index=mock_index)
        assert sceneaction.act == do_nothing
        assert not sceneaction.can_set_runtime
        assert sceneaction.transform.args == mock_args
        assert sceneaction.transform.transform == mock_fn
        assert sceneaction.transform.color_index == mock_index

class TestAlgoTransform:

    def test_set_color_does_nothing_if_cannot_set_color(self):
        transform = AlgoTransform(mock_args)
        transform.set_color('#00000')
        assert transform.color_index is None

    def test_set_color_only_if_can_set_color(self):
        old_color = '#00001'
        transform = AlgoTransform([old_color], color_index=0)
        color = '#00000'
        transform.set_color(color)
        assert transform.args[transform.color_index] == color

    def test_run_returns_args_if_no_transform(self):
        transform = AlgoTransform(mock_args)
        assert transform.run() == mock_args

    def test_run_runs_transform(self):
        args = [mock_args]
        transform = AlgoTransform(args, transform=mock_fn)
        mock_args.reset_mock()
        mock_fn.reset_mock()

        transform.run()

        mock_fn.assert_called_once_with(*args)
