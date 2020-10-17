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
    def __init__(self, act, *transforms, w_prev=False):
        self.act = act
        self.transforms = transforms
        self.w_prev = w_prev

    def add_transforms(self, *transforms):
        self.transforms += transforms

    def change_color(self, new_color):
        for transform in self.transforms:
            transform.change_color(new_color)

    def run(self):
        args = []
        for transform in self.transforms:
            result = transform.generate()
            if isinstance(result, list):
                for arg in result:
                    args.append(arg)
            else:
                args.append(result)
        self.act(*args)

class AlgoScene(Scene):
    def algoconstruct(self):
        pass

    def add_action(self, act, *transforms, w_prev=False):
        action = AlgoSceneAction(act, *transforms, w_prev=w_prev)
        self.actions.append(action)

    def construct(self):
        self.actions = []
        self.anim_grps = []
        self.algoconstruct()
        for (i, action) in enumerate(self.actions):
            for action2 in self.actions[i+1:]:
                if action2.w_prev:
                    if action2.act == action.act:
                        action.add_transforms(*action2.transforms)
                        self.actions.remove(action2)
                else:
                    break
            action.run()
