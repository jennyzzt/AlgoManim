# pylint: disable=R0903
from manimlib.imports import Scene

class AlgoSceneAction:
    def __init__(self, act, *args, w_prev=False):
        self.act = act
        self.args = args
        self.w_prev = w_prev

    def add_args(self, *args):
        self.args += args

    def run(self):
        self.act(*self.args)

class AlgoScene(Scene):
    def algoconstruct(self):
        pass

    def add_action(self, act, *args, w_prev=False):
        action = AlgoSceneAction(act, *args, w_prev=w_prev)
        self.actions.append(action)

    def construct(self):
        self.actions = []
        self.anim_grps = []
        self.algoconstruct()
        for (i, action) in enumerate(self.actions):
            for action2 in self.actions[i+1:]:
                if action2.w_prev:
                    if action2.act == action.act:
                        action.add_args(*action2.args)
                        self.actions.remove(action2)
                else:
                    break
            action.run()
