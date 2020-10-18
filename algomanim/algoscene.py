# pylint: disable=R0903
from manimlib.imports import *

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

    def change_color(self, new_color):
        if self.color_index is None:
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
    def __init__(self, anim_action, action, run_time=None):
        '''
        encodes a pair of AlgoSceneActions
        if run_time is None, anim_action is run
        else if run_time == 0, action is run
        else if run_time > 0, anim_action is run with a run_time parameter
        '''
        self.anim_action = anim_action
        self.action = action
        self.run_time = run_time

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

        return self.action

    def act(self):
        return self.curr_action().act

    def run(self):
        self.curr_action().run(self.run_time)

    def change_color(self, new_color):
        self.anim_action.change_color(new_color)
        self.action.change_color(new_color)

class AlgoScene(Scene):
    def algoconstruct(self):
        pass

    def add_action_pair(self, anim_action, action, run_time=None):
        self.action_pairs.append(AlgoSceneActionPair(anim_action, action, run_time))

    def skip(self, start, end=None):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.skip()

    def add_wait(self, index, wait_time=1):
        anim_action = AlgoSceneAction(self.wait, AlgoTransform([wait_time]))
        action = AlgoSceneAction(lambda x: x, AlgoTransform([1])) # dummy function to skip wait
        self.action_pairs.insert(index, AlgoSceneActionPair(anim_action, action))

    def fast_forward(self, start, end=None, speed_up=2):
        if end is None:
            end = len(self.action_pairs)

        for action_pair in self.action_pairs[start:end]:
            action_pair.fast_forward(speed_up)

    def construct(self):
        self.action_pairs = []
        self.anim_grps = []
        self.algoconstruct()
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

        if len(self.action_pairs) > 0:
            last_action_pair = self.action_pairs[-1]
            last_act = last_action_pair.act()
            if last_act != self.play or last_act != self.wait or last_action_pair.run_time is None: # pylint: disable=W0143
                # wait action is required at the end if last animation is not
                # a play/wait or has been skipped, else the last animation will not be rendered
                self.wait()
