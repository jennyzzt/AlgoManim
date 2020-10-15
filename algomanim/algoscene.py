# pylint: disable=R0903
from manimlib.imports import Scene

class AlgoSceneAction:
    def __init__(self, act, *args):
        self.act = act
        self.args = args

class AlgoScene(Scene):
    def algoconstruct(self):
        pass

    def add_action(self, act, *args, w_prev=False):
        action = AlgoSceneAction(act, *args)
        if w_prev and action.act == self.actions[-1].act:
            self.actions[-1].args += args
        else:
            self.actions.append(action)

    def construct(self):
        self.actions = []
        self.anim_grps = []
        self.algoconstruct()
        for action in self.actions:
            action.act(*action.args)
