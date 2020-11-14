from manimlib.imports import *
from gui.panels.customisation_type import CustomisationType


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
