# pylint: disable=R0903, R0904
from manimlib.imports import *
from algomanim.settings import DEFAULT_SETTINGS
from gui.panels.customisation_type import CustomisationType
from .animation_block import AnimationBlock
from .metadata_block import MetadataBlock
from .metadata import Metadata, LowerMetadata

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
        """
        if transform is None, this class encapsulates a list of arguments
        else, the arguments are to be consumed by the transform function
        if color_index is None, this transform does not have a color property
        else, color can be changed by changing args[color_index]
        """
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
    def create_empty_action(args=[]): # pylint: disable=W0102
        # empty filler action
        return AlgoSceneAction.create_static_action(do_nothing, args)

    def __init__(self, act, transform=None, w_prev=False, can_set_runtime=False):
        self.act = act
        self.transform = transform
        self.w_prev = w_prev
        self.can_set_runtime = can_set_runtime

    def get_args(self):
        return self.transform.args

    def can_set_color(self):
        if self.transform is not None:
            return self.transform.can_set_color()

        return False

    def set_color(self, color):
        if self.transform is not None:
            self.transform.set_color(color)

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

    def get_args(self):
        return self.curr_action().get_args()

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

        if self.can_set_runtime() and self.anim_block.first_pair() == self:
            # runtime argument is only used when the runtime argument can be set
            # and action_pair is the first pair in block
            customizations[CustomisationType.RUNTIME] = self.get_runtime_val()

        return customizations

class AlgoScene(Scene):
    def __init__(self, **kwargs):
        # Default settings
        self.settings = DEFAULT_SETTINGS.copy()

        # Used to reobtain objects that are removed by certain animations
        self.save_mobjects = None

        # Tracker for all items in the Scene
        self.algo_objs = []

        self.kwargs = kwargs
        self.post_customize_fns = kwargs.get('post_customize_fns', [])
        self.post_config_settings = kwargs.get('post_config_settings', {})

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
        settings.update(self.post_config_settings)

    def create_play_action(self, transform, w_prev=False):
        return AlgoSceneAction(
            self.play, transform,
            w_prev=w_prev, can_set_runtime=True
        )

    def add_action_pair(self, anim_action, static_action=None, animated=True, index=None):
        pair = AlgoSceneActionPair(anim_action, static_action,
                                   run_time=None if animated else 0)
        self.insert_action_pair(pair, index)
        return pair

    def insert_action_pair(self, action_pair, index=None):
        if index is not None:
            self.push_back_action_pair_indices(index)
        else:
            index = len(self.action_pairs)

        action_pair.attach_index(index)
        self.action_pairs.insert(index, action_pair)

    def add_metadata(self, metadata):
        self.meta_trees.append(metadata)

    # Add item so they can subscribe themselves to scene transformations like Shifts
    def track_algoitem(self, algo_item):
        self.algo_objs.append(algo_item)

    def remove_algoitem(self, algo_item):
        if algo_item in self.algo_objs:
            self.algo_objs.remove(algo_item)

    def shift_scene(self, vector, metadata=None):
        first = True

        for algo_obj in self.algo_objs:
            # Shift all items UP
            if first:
                algo_obj.set_next_to(algo_obj, vector, metadata, animated=True, w_prev=False)
                first = False
            else:
                algo_obj.set_next_to(algo_obj, vector, metadata, animated=True, w_prev=True)

    def skip(self, start, end=None):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.skip()

    def push_back_action_pair_indices(self, index):
        for action_pair in self.action_pairs[index:]:
            action_pair.attach_index(action_pair.get_index() + 1)

    def add_transform(self, index, transform, args=[], metadata=None): # pylint: disable=W0102
        anim_action = self.create_play_action(AlgoTransform(args, transform=transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.insert_action_pair(action_pair, index)

        if metadata is None:
            curr_metadata = Metadata('custom')
            lower_meta = LowerMetadata('custom', action_pair)
            curr_metadata.add_lower(lower_meta)

            self.add_metadata(curr_metadata)
        else:
            self.add_metadata(metadata)

    # Convenience function to add a text object and the Write transform
    # Returns the created text object
    def add_text(self, text, index, position=UP):
        text = TextMobject(text)
        text.shift(2 * position)
        transform = lambda: Write(text)
        self.add_transform(index, transform)
        return text

    # Convenience function to edit existing text objects via a ReplacementTransform
    # Requires the previous text object to be edited
    # Returns the replacement text object
    def change_text(self, new_text_string, old_text_object, index, position=UP):
        new_text_object = TextMobject(new_text_string)
        new_text_object.shift(2 * position)

        # Create the transform to be run at that point
        transform = lambda old_text, new_text: \
            [FadeOut(old_text), ReplacementTransform(old_text, new_text)]
        self.add_transform(index, transform, args=[old_text_object, new_text_object])
        return new_text_object

    # Convenience function to FadeOut an existing text object
    def remove_text(self, old_text_object, index):
        transform = lambda: FadeOut(old_text_object)
        self.add_transform(index, transform)

    def add_static(self, index, static_fn, args=[], metadata=None): # pylint: disable=W0102
        static_action = AlgoSceneAction.create_static_action(static_fn, args)
        action_pair = AlgoSceneActionPair(static_action, static_action)
        self.insert_action_pair(action_pair, index)

        if metadata is None:
            curr_metadata = Metadata('custom')
            lower_meta = LowerMetadata('custom', action_pair)
            curr_metadata.add_lower(lower_meta)
            self.add_metadata(curr_metadata)
        else:
            self.add_metadata(metadata)

    def add_fade_out_all(self, index):
        anim_action = self.create_play_action(AlgoTransform([self], transform=fade_out_transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.insert_action_pair(action_pair, index)

        curr_metadata = Metadata('fade_out')
        lower_meta = LowerMetadata('fade_out', action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_fade_in_all(self, index):
        anim_action = self.create_play_action(AlgoTransform([self], transform=fade_in_transform))
        action_pair = AlgoSceneActionPair(anim_action, anim_action)
        self.insert_action_pair(action_pair, index)

        curr_metadata = Metadata('fade_in')
        lower_meta = LowerMetadata('fade_in', action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_wait(self, index, wait_time=1):
        anim_action = AlgoSceneAction(self.wait, AlgoTransform([wait_time]))
        # Using a dummy function to skip wait
        static_action = AlgoSceneAction.create_empty_action()
        action_pair = AlgoSceneActionPair(anim_action, static_action)
        self.insert_action_pair(action_pair, index)

        curr_metadata = Metadata('wait')
        lower_meta = LowerMetadata('wait', action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

    def add_clear(self, index):
        action = AlgoSceneAction.create_static_action(self.clear)
        self.insert_action_pair(AlgoSceneActionPair(action), index)

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
                # wait action is required at the end if last animation is not
                # a play/wait, else the last animation will not be rendered
                self.add_wait(len(self.action_pairs))

        # attach indexes to action_pair to be used in GUI
        # customizations
        for (i, action_pair) in enumerate(action_pairs):
            action_pair.attach_index(i)

        # run post customize functions from the GUI
        for post_customize in self.post_customize_fns:
            post_customize(self)

        # bundle animations together according to time
        self.create_animation_blocks(action_pairs, anim_blocks)

        # and run them
        for anim_block in self.anim_blocks:
            anim_block.run()

    def create_metadata_blocks(self):
        self.metadata_blocks = []

        for tree in self.meta_trees:
            action_pairs = tree.get_all_action_pairs()

            blocks = {action_pair.get_block() for action_pair in action_pairs}
            if len(blocks) == 0:
                print(f'WARNING: Metadata: {tree.desc(sep=" ")} \
                    has no action_pairs attached to it!')
            else:
                start_time = min(map(lambda block: block.start_time, blocks))
                end_time = max(map(lambda block: block.start_time + block.runtime_val(), blocks))

                runtime = end_time - start_time

                self.metadata_blocks.append(
                    MetadataBlock(tree, action_pairs, start_time, runtime)
                )

        # some metadata might be added out of order, sort the blocks by start_time
        self.metadata_blocks.sort(key = lambda meta_block: meta_block.start_time)

    def insert_pin(self, desc, *args):
        empty_action = AlgoSceneAction.create_empty_action(list(args))
        empty_pair = self.add_action_pair(empty_action)

        lower_meta = LowerMetadata(desc, empty_pair)
        metadata = Metadata(desc)
        metadata.add_lower(lower_meta)

        self.add_metadata(metadata)

    def find_pin(self, desc):
        action_pairs = self.find_action_pairs(desc)
        return action_pairs

    def find_action_pairs(self, method, occurence=None, lower_level=None):
        action_pairs = []
        for meta_tree in self.meta_trees:
            if method == meta_tree.metadata and (occurence is None or occurence == meta_tree.fid):
                if lower_level:
                    for lower in meta_tree.children:
                        if lower_level == lower.metadata:
                            action_pairs.append(lower.action_pair)
                else:
                    for action_pair in meta_tree.get_all_action_pairs():
                        action_pairs.append(action_pair)
        return action_pairs

    def construct(self):
        Metadata.reset_counter()
        self.preconfig(self.settings)
        self.post_config(self.settings)

        self.algoconstruct()
        self.customize(self.action_pairs)

        self.execute_action_pairs(self.action_pairs, self.anim_blocks)
        self.create_metadata_blocks()
