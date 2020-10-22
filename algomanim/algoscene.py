# pylint: disable=R0903
from manimlib.imports import *
from algomanim.settings import DEFAULT_SETTINGS

class AlgoTransform:
    def __init__(self, args, transform=None, color_index=None):
        '''
        if transform is None, this class encapsulates a list of arguments
        else, the arguments are for the transform constructor
        if color_index is None, this transform does not have a color property
        else, color can be changed by changing args[color_index]
        '''
        self.transform = transform
        self.args = args
        self.color_index = color_index

    def can_change_color(self):
        return self.color_index is not None

    def change_color(self, new_color):
        if not self.can_change_color():
            print('WARNING: Transform does not have color property')
            return

        self.args[self.color_index] = new_color

    def generate(self):
        if self.transform is None:
            return self.args

        return self.transform(*self.args)

class AlgoSceneAction:
    def __init__(self, act, *transforms, w_prev=False, can_change_runtime=False):
        self.act = act
        self.transforms = transforms
        self.w_prev = w_prev
        self.can_change_runtime = can_change_runtime

    def add_transforms(self, *transforms):
        self.transforms += transforms

    def can_change_color(self):
        can_change_color = False

        # if a transform can change color, action can change color
        for transform in self.transforms:
            if transform.can_change_color():
                can_change_color = True
                break

        return can_change_color

    def change_color(self, new_color):
        for transform in self.transforms:
            transform.change_color(new_color)

    def run(self, run_time=None):
        args = []
        for transform in self.transforms:
            result = transform.generate()
            if isinstance(result, list):
                for arg in result:
                    args.append(arg)
            else:
                args.append(result)

        if run_time is None or not self.can_change_runtime:
            self.act(*args)
        else:
            self.act(*args, run_time=run_time)

class AlgoSceneActionPair:
    def __init__(self, anim_action, static_action=None, run_time=None, metadata=None):
        '''
        encodes a pair of AlgoSceneActions
        if run_time is None, anim_action is run
        else if run_time == 0, static_action is run
        else if run_time > 0, anim_action is run with a run_time parameter
        '''
        self.anim_action = anim_action
        self.static_action = static_action if static_action is not None else anim_action
        self.run_time = run_time
        self.metadata = metadata

    def can_change_runtime(self):
        return self.anim_action.can_change_runtime

    def can_change_color(self):
        return self.anim_action.can_change_color()

    def skip(self):
        self.run_time = 0

    def fast_forward(self, speed_up = 2):
        if self.run_time is None:
            self.run_time = 1 / speed_up
        else:
            self.run_time /= speed_up

    def curr_action(self):
        if self.run_time is None or self.run_time > 0:
            return self.anim_action

        return self.static_action

    def act(self):
        return self.curr_action().act

    def run(self):
        self.curr_action().run(self.run_time)

    def change_color(self, new_color):
        self.anim_action.change_color(new_color)
        self.static_action.change_color(new_color)

class AlgoScene(Scene):
    # Used to reobtain objects that are removed by certain animations
    save_mobjects = None

    # Default settings
    settings = DEFAULT_SETTINGS

    def preconfig(self, settings):
        pass

    def algoconstruct(self):
        pass

    def customize(self, action_pairs):
        pass

    def create_play_action(self, *transforms, w_prev=False):
        return AlgoSceneAction(
            self.play, *transforms,
            w_prev=w_prev, can_change_runtime=True
        )

    def add_action_pair(self, anim_action, static_action, animated=True, metadata=None):
        self.action_pairs.append(
            AlgoSceneActionPair(anim_action, static_action, run_time=None if animated else 0, metadata=metadata)
        )

    def skip(self, start, end=None):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.skip()

    def add_transform(self, index, transform):
        anim_action = self.create_play_action(AlgoTransform([], transform=transform))
        # Using a dummy function to skip wait
        static_action = AlgoSceneAction(lambda x: x, AlgoTransform([1]))
        self.action_pairs.insert(index, AlgoSceneActionPair(anim_action, static_action))

    def add_wait(self, index, wait_time=1):
        anim_action = AlgoSceneAction(self.wait, AlgoTransform([wait_time]))
        # Using a dummy function to skip wait
        static_action = AlgoSceneAction(lambda x: x, AlgoTransform([1]))
        self.action_pairs.insert(index, AlgoSceneActionPair(anim_action, static_action))

    def add_clear(self, index):
        action = AlgoSceneAction(self.clear, AlgoTransform([]))
        self.action_pairs.insert(index, AlgoSceneActionPair(action))

    def fast_forward(self, start, end=None, speed_up=2):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.fast_forward(speed_up)

    def construct(self):
        self.preconfig(self.settings)
        self.action_pairs = []
        self.algoconstruct()
        self.customize(self.action_pairs)

        if len(self.action_pairs) > 0:
            last_action_pair = self.action_pairs[-1]
            last_act = last_action_pair.act()
            if last_act != self.play or last_act != self.wait or last_action_pair.run_time == 0: # pylint: disable=W0143
                # wait action is required at the end if last animation is not
                # a play/wait or has been skipped, else the last animation will not be rendered
                self.add_wait(len(self.action_pairs))

        # save a copy of action_pairs
        action_pairs_copy = self.action_pairs.copy()

        # start executing actions
        for (i, action_pair) in enumerate(self.action_pairs):
            action = action_pair.curr_action()
            for action_pair2 in self.action_pairs[i+1:]:
                action2 = action_pair2.curr_action()
                if action2.w_prev:
                    if action2.act == action.act:
                        action.add_transforms(*action2.transforms)
                        self.action_pairs.remove(action_pair2)
                else:
                    break
            action_pair.run()

        # restore copy of action_pairs so that this information can be used post rendering
        self.action_pairs = action_pairs_copy
