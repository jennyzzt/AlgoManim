# pylint: disable=R0903
from manimlib.imports import *
from algomanim.settings import DEFAULT_SETTINGS
from gui.panels.customisation_type import CustomisationType
from .animation_block import AnimationBlock
from .metadata_block import MetadataBlock
from .metadata import Metadata, AlgoListMetadata, LowerMetadata

def do_nothing(*_):
    return

def fade_out_transform(scene):
    scene.save_mobjects = scene.mobjects
    return list(map(FadeOut, scene.save_mobjects))

def fade_in_transform(scene):
    result = list(map(FadeIn, scene.save_mobjects))
    scene.save_mobjects = []
    return result

class AlgoTransform:
    def __init__(self, args, transform=None, color_index=None):
        '''
        if transform is None, this class encapsulates a list of arguments
        else, the arguments are to be consumed by the transform function
        if color_index is None, this transform does not have a color property
        else, color can be changed by changing args[color_index]
        '''
        self.transform = transform
        self.args = args
        self.color_index = color_index

    def can_set_color(self):
        return self.color_index is not None

    def get_color(self):
        if not self.can_set_color():
            print('WARNING: Transform does not have color property')
            return None

        return self.args[self.color_index]

    def set_color(self, color):
        if not self.can_set_color():
            print('WARNING: Transform does not have color property')
            return

        self.args[self.color_index] = color

    def run(self):
        if self.transform is None:
            return self.args

        return self.transform(*self.args)

class AlgoSceneAction:
    @staticmethod
    def create_static_action(function, args=[], color_index=None): # pylint: disable=W0102
        # w_prev flag does not matter for static actions
        return AlgoSceneAction(
            do_nothing,
            transform=AlgoTransform(args, transform=function, color_index=color_index),
            w_prev=True,
            can_set_runtime=False)

    @staticmethod
    def create_empty_action():
        # empty filler action
        return AlgoSceneAction.create_static_action(do_nothing, [])

    def __init__(self, act, transform=None, w_prev=False, can_set_runtime=False):
        self.act = act
        self.transform = transform
        self.w_prev = w_prev
        self.can_set_runtime = can_set_runtime

    def can_set_color(self):
        if self.transform is not None:
            return self.transform.can_set_color()

        return False

    def set_color(self, color):
        if self.transform is not None:
            return self.transform.set_color(color)

    def get_color(self):
        if self.transform is not None:
            return self.transform.get_color()

        return None

    def run(self):
        if self.transform is not None:
            return self.transform.run()
        return []

class AlgoSceneActionPair:
    def __init__(self, anim_action, static_action=None, run_time=None):
        '''
        encodes a pair of AlgoSceneActions
        if run_time is None, anim_action is run
        else if run_time == 0, static_action is run
        else if run_time > 0, anim_action is run with a run_time parameter
        '''
        self.anim_action = anim_action
        self.static_action = static_action if static_action is not None else anim_action
        self.run_time = run_time
        self.anim_block = None # anim_block this action_pair ends up in
        self.index = None # index of action pair in action_pairs list

    def attach_block(self, anim_block):
        self.anim_block = anim_block

    def attach_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def get_block(self):
        return self.anim_block

    def can_set_runtime(self):
        return self.anim_action.can_set_runtime

    def get_runtime(self):
        return self.run_time

    def get_runtime_val(self):
        if not self.can_set_runtime():
            return 0

        return 1 if self.run_time is None else self.run_time

    def set_runtime(self, run_time):
        if not self.can_set_runtime() and run_time != 0:
            print('WARNING: ActionPair does not have runtime property')
            return

        if self.anim_action == self.static_action and run_time == 0:
            print('WARNING: ActionPair cannot be skipped')
            return

        if not isinstance(run_time, float) or not isinstance(run_time, int):
            run_time = float(run_time)

        self.run_time = run_time

    def can_set_color(self):
        return self.anim_action.can_set_color() or \
            self.static_action.can_set_color()

    def get_color(self):
        return self.anim_action.get_color()

    def set_color(self, color):
        self.anim_action.set_color(color)
        self.static_action.set_color(color)

    def skip(self):
        self.set_runtime(0)

    def fast_forward(self, speed_up = 2):
        if self.run_time is None:
            self.set_runtime(1 / speed_up)
        else:
            self.set_runtime(self.run_time / speed_up)

    def curr_action(self):
        if self.run_time is None or self.run_time > 0:
            return self.anim_action

        return self.static_action

    def act(self):
        return self.curr_action().act

    def run(self):
        return self.curr_action().run()

    def customizations(self):
        customizations = dict()
        if self.can_set_color():
            customizations[CustomisationType.COLOR] = self.get_color()

        if self.can_set_runtime():
            customizations[CustomisationType.RUNTIME] = self.get_runtime_val()

        return customizations

class AlgoScene(Scene):
    def __init__(self, **kwargs):
        # Default settings
        self.settings = DEFAULT_SETTINGS.copy()

        # Used to reobtain objects that are removed by certain animations
        self.save_mobjects = None

        self.kwargs = kwargs
        if not hasattr(self, 'post_customize_fns'):
            # when rerendering, do not set this list back to []
            self.post_customize_fns = []

        self.action_pairs = []
        self.anim_blocks = []
        self.meta_trees = []
        self.metadata_blocks = []

        Scene.__init__(self, **kwargs)

    def preconfig(self, settings):
        pass

    def algoconstruct(self):
        pass

    def customize(self, action_pairs):
        pass

    def post_config(self, settings):
        pass

    def rerender(self):
        self.__init__(**self.kwargs)

    def create_play_action(self, transform, w_prev=False):
        return AlgoSceneAction(
            self.play, transform,
            w_prev=w_prev, can_set_runtime=True
        )

    def add_action_pair(self, anim_action, static_action, animated=True):
        pair = AlgoSceneActionPair(anim_action, static_action,
                                   run_time=None if animated else 0)
        self.action_pairs.append(pair)
        return pair

    def add_metadata(self, metadata):
        self.meta_trees.append(metadata)

    def skip(self, start, end=None):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.skip()

    def add_transform(self, index, transform, metadata=None):
        anim_action = self.create_play_action(AlgoTransform([], transform=transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.action_pairs.insert(index, action_pair)

        if metadata is None:
            curr_metadata = Metadata(AlgoListMetadata.CUSTOM)
            lower_meta = LowerMetadata(AlgoListMetadata.CUSTOM, action_pair)
            curr_metadata.add_lower(lower_meta)

            self.add_metadata(curr_metadata)
        else:
            self.add_metadata(metadata)

    def add_fade_out_all(self, index):
        anim_action = self.create_play_action(AlgoTransform([self], transform=fade_out_transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.action_pairs.insert(index, action_pair)

        curr_metadata = Metadata(AlgoListMetadata.FADE_OUT)
        lower_meta = LowerMetadata(AlgoListMetadata.FADE_OUT, action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_fade_in_all(self, index):
        anim_action = self.create_play_action(AlgoTransform([self], transform=fade_in_transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.action_pairs.insert(index, action_pair)

        curr_metadata = Metadata(AlgoListMetadata.FADE_IN)
        lower_meta = LowerMetadata(AlgoListMetadata.FADE_IN, action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_wait(self, index, wait_time=1):
        anim_action = AlgoSceneAction(self.wait, AlgoTransform([wait_time]))
        # Using a dummy function to skip wait
        static_action = AlgoSceneAction.create_empty_action()
        action_pair = AlgoSceneActionPair(anim_action, static_action)
        self.action_pairs.insert(index, action_pair)

        curr_metadata = Metadata(AlgoListMetadata.WAIT)
        lower_meta = LowerMetadata(AlgoListMetadata.WAIT, action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_clear(self, index):
        action = AlgoSceneAction.create_static_action(self.clear)
        self.action_pairs.insert(index, AlgoSceneActionPair(action))

    def fast_forward(self, start, end=None, speed_up=2):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.fast_forward(speed_up)

    def create_animation_blocks(self, action_pairs, anim_blocks): # pylint: disable=R0201
        # convert action_pairs into anim_blocks
        start_time = 0
        for action_pair in action_pairs:
            action = action_pair.curr_action()
            if action.w_prev and len(anim_blocks) > 0 and anim_blocks[-1].act() == action.act:
                # if action is supposed to be executed with previous action and
                # act function is the same as that of current block, bundle actions
                # together
                anim_blocks[-1].add_action_pair(action_pair)
            else:
                # else, create new Animation Block
                anim_blocks.append(AnimationBlock([action_pair], start_time))
                start_time += anim_blocks[-1].runtime_val()

            # attach block to action pair so that time data can be
            # extracted later to be used in GUI
            action_pair.attach_block(anim_blocks[-1])

    def execute_action_pairs(self, action_pairs, anim_blocks):
        # wait action is required at the end if last animation is not
        # a play/wait, else the last animation will not be rendered
        if len(action_pairs) > 0:
            last_action_pair = action_pairs[-1]
            last_act = last_action_pair.act()
            if last_act != self.play or last_act != self.wait: # pylint: disable=W0143
                self.add_wait(len(self.action_pairs))

        # attach indexes to action_pair to be used in GUI
        # customizations
        for (i, action_pair) in enumerate(action_pairs):
            action_pair.attach_index(i)

        # run post customize functions from the GUI
        for post_customize in self.post_customize_fns:
            post_customize(self.action_pairs)

        # bundle animations together according to time
        self.create_animation_blocks(action_pairs, anim_blocks)

        # and run them
        for anim_block in self.anim_blocks:
            anim_block.run()

    def create_metadata_blocks(self):
        self.metadata_blocks = []

        for tree in self.meta_trees:
            action_pairs = tree.get_all_action_pairs()

            blocks = list({action_pair.get_block() for action_pair in action_pairs})
            start_time = blocks[0].start_time
            end_time = blocks[-1].start_time + blocks[-1].runtime_val()
            runtime = end_time - start_time

            self.metadata_blocks.append(
                MetadataBlock(tree, action_pairs, start_time, runtime)
            )
        # some metadata might be added out of order, sort the blocks by start_time
        self.metadata_blocks.sort(key = lambda meta_block: meta_block.start_time)

    def construct(self):
        Metadata.reset_counter()
        self.preconfig(self.settings)
        self.post_config(self.settings)

        self.algoconstruct()
        self.customize(self.action_pairs)

        self.execute_action_pairs(self.action_pairs, self.anim_blocks)
        self.create_metadata_blocks()
