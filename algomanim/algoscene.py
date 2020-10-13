from manimlib.imports import Scene

class AlgoScene(Scene):
    def algoconstruct(self):
        pass

    def add_anim_grp(self, *anims, together_with_prev=False):
        if together_with_prev and len(self.anim_grps) > 0:
            self.anim_grps[-1] += anims
        else:
            self.anim_grps.append(anims)

    def construct(self):
        self.anim_grps = []
        self.algoconstruct()
        for anim_grp in self.anim_grps:
            self.play(*anim_grp)