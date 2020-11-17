# pylint: disable=R0914, W0122, W0105, R0904
import ast
import inspect
from collections import namedtuple
from manimlib.imports import *
from algomanim.settings import DEFAULT_SETTINGS
from algomanim.algoaction import AlgoTransform, AlgoSceneAction, AlgoSceneActionPair, \
    fade_in_transform, fade_out_transform
from .animation_block import AnimationBlock
from .metadata_block import MetadataBlock
from .metadata import Metadata, LowerMetadata


# ----- import utility used for code_anim ----- #
Import = namedtuple("Import", ["module", "name", "alias"])

def get_imports(path):
    with open(path) as path_file:
        root = ast.parse(path_file.read(), path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')
        else:
            continue

        for node_name in node.names:
            yield Import(module, node_name.name.split('.'), node_name.asname)
# --------------------------------------------- #

class AlgoScene(MovingCameraScene):
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

        MovingCameraScene.__init__(self, **kwargs)

    def is_code_anim(self):
        return self.settings['code_anim']

    ''' For user to overwrite '''
    def preconfig(self, settings):
        pass

    def algo_codeanim(self):
        # import necessary modules
        file_path = inspect.getsourcefile(self.algo)
        imports = get_imports(file_path)
        for imp in imports:
            module = '.'.join(imp.module)
            names = ','.join(imp.name)
            if imp.module:
                exec(f'from {module} import {names}')
            else:
                exec(f'import {names}')
        # get algo source lines
        source_lines, _ = inspect.getsourcelines(self.algo)

        algo_source_lines = []
        modified_source_lines = []

        # get redundant spacing for first code line that is not def
        redundant_space_count = len(source_lines[1]) - len(source_lines[1].lstrip())
        # insert pin at every alternate source line
        for i, line in enumerate(source_lines):
            front_space_count = len(line) - len(line.lstrip())

            # Do not execute first def line, empty line, or comment
            if i == 0 or not line.strip() or line[front_space_count] == '#':
                continue

            line_tab = ' ' * (front_space_count - redundant_space_count)

            # If inner fn, add global declaration
            if line[front_space_count:].split()[0] == 'def':
                inner_fn_name = line[front_space_count:].split()[1]
                inner_fn_name = inner_fn_name.split('(')[0]
                modified_source_lines.append(f'{line_tab}global {inner_fn_name}\n')

            # Insert pin if line is not a pin
            elif 'insert_pin' not in line:
                pin = f'{line_tab}self.insert_pin(\'__codeindex__\', {len(algo_source_lines)})\n'
                modified_source_lines.append(pin)

            # Add original code
            algo_source_lines.append(line)
            modified_source_lines.append(line[redundant_space_count:])

        # insert pin at the beginning to show all code
        sourcecode = [line.replace('\n', '') for line in algo_source_lines]
        pin_code_source = f'self.insert_pin(\'__sourcecode__\', {sourcecode})\n'
        modified_source_lines.insert(0, pin_code_source)

        # get modified source code and execute
        modified_source_code = ''.join(modified_source_lines)
        exec(f'{modified_source_code}')

    def algo_construct(self):
        # Add parallel code animation
        if self.is_code_anim():
            self.algo_codeanim()
        # Run normal algo animation
        else:
            self.algo()

    ''' For user to overwrite '''
    def algo(self):
        pass

    def customize_codeanim(self):
        # ----- helper static fns ----- #
        def zoom_out():
            new_center = self.camera_frame.get_right()
            self.camera_frame.set_width(self.camera_frame.get_width() * 2)
            self.camera_frame.move_to(new_center)

        def show_sourcecode(textobjs, num_spaces):
            if not textobjs or not num_spaces:
                return
            # move first line to the desired position
            mid_index = len(textobjs)/2
            textobjs[0].move_to((self.camera_frame.get_center() +
                                 self.camera_frame.get_right()) / 2)
            textobjs[0].shift(mid_index * UP * 0.7)
            # arrange text group downwards aligned to the left
            text = VGroup(*textobjs)
            text.arrange(DOWN, center=False, aligned_edge=LEFT)
            # add tabbing to shown text
            for i, textobj in enumerate(textobjs):
                textobj.shift(num_spaces[i] * RIGHT)
            # add text
            self.add(text)

        def add_arrow_beside(arrow, textobj):
            arrow.next_to(textobj, LEFT)
            self.add(arrow)
        # ----------------------------- #

        # zoom camera out
        self.add_static(0, zoom_out)

        # show source code text
        sourcecode_pin = self.find_pin('__sourcecode__')[0]
        index = sourcecode_pin.get_index()
        sourcecode = sourcecode_pin.get_args()[0]
        num_spaces = [len(line) - len(line.lstrip(' ')) for line in sourcecode]
        min_spaces = min([n for n in num_spaces if n != 0])
        num_spaces = [(n / min_spaces - 1) for n in num_spaces]
        textobjs = [Text(line.lstrip(), font='Inconsolata') for line in sourcecode]
        self.add_static(index, show_sourcecode, [textobjs, num_spaces])

        # move arrow to which code line is executed
        arrow = Arrow(ORIGIN, RIGHT)
        self.add_static(index+1, add_arrow_beside, [arrow, textobjs[0]])
        codeindex_pins = self.find_pin('__codeindex__')
        for pin in codeindex_pins:
            index = pin.get_index()
            codeindex = pin.get_args()[0]
            self.add_transform(index, ApplyMethod, args=[arrow.next_to,
                                                         textobjs[codeindex], LEFT])

    def customize_construct(self, action_pairs):
        # Add customisation needed for parallel code anim
        if self.is_code_anim():
            self.customize_codeanim()
        # Run user-defined customize fn
        self.customize(action_pairs)

    ''' For user to overwrite '''
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

    def untrack_algoitem(self, algo_item):
        if algo_item in self.algo_objs:
            self.algo_objs.remove(algo_item)

    def shift_scene(self, vector, metadata=None):
        first = True

        for algo_obj in self.algo_objs:
            # Shift all items UP
            if first:
                algo_obj.set_next_to(algo_obj, vector, metadata=metadata, animated=True,
                    w_prev=False)
                first = False
            else:
                algo_obj.set_next_to(algo_obj, vector, metadata=metadata, animated=True,
                    w_prev=True)

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
        text.shift(position)
        transform = lambda: Write(text)
        self.add_transform(index, transform)
        return text

    # Convenience function to edit existing text objects via a ReplacementTransform
    # Requires the previous text object to be edited
    # Returns the replacement text object
    def change_text(self, new_text_string, old_text_object, index=None):
        position = old_text_object.get_center()
        new_text_object = TextMobject(new_text_string)
        new_text_object.shift(position)

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

    def add_slide(self, text, index, text_position=ORIGIN, duration=1.0):
        self.add_fade_out_all(index)
        text_anim = self.add_text(text, index + 1, position=text_position)
        self.add_wait(index + 2, wait_time=duration)
        self.remove_text(text_anim, index + 3)
        self.add_fade_in_all(index + 4)

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
        action_pair = AlgoSceneAction.create_static_action(self.clear)
        self.insert_action_pair(AlgoSceneActionPair(action_pair), index)

        curr_metadata = Metadata('clear')
        lower_meta = LowerMetadata('clear', action_pair)
        curr_metadata.add_lower(lower_meta)

        self.add_metadata(curr_metadata)

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
            if action.w_prev and anim_blocks and anim_blocks[-1].act() == action.act:
                # anim_blocks should have at least 1 element
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

        if action_pairs:
            # action_pairs should not be empty
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
            if not blocks:
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

        self.algo_construct()
        self.customize_construct(self.action_pairs)

        self.execute_action_pairs(self.action_pairs, self.anim_blocks)
        self.create_metadata_blocks()
