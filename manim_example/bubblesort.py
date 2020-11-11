#!/usr/bin/env python
# pylint: disable=E0602

from manimlib.imports import *

class BubbleSortManimScene(Scene):
    def init_list(self, input_list):
        nodes = []

        for i in input_list:
            sqr = Square(
                fill_color=WHITE,
                fill_opacity=1,
                side_length=1.5
            )
            txt = TextMobject(str(i))
            txt.set_color(BLACK)
            grp = VGroup(sqr, txt)
            nodes.append(grp)

        for i in range(1, len(nodes)):
            nodes[i].next_to(nodes[i - 1], RIGHT)

        for node in nodes:
            self.add(node)

        nodes_grp = VGroup(*nodes)
        self.play(nodes_grp.center)
        return nodes

    def construct(self):
        input_list = [25, 43, 5, 18, 30]
        nodes = self.init_list(input_list)

        swaps_made = True

        while swaps_made:
            swaps_made = False
            for i in range(len(nodes) - 1):
                j = i + 1

                sqr1 = nodes[i].__getitem__(0)
                sqr2 = nodes[j].__getitem__(0)
                val1 = int(nodes[i].__getitem__(1).get_tex_string())
                val2 = int(nodes[j].__getitem__(1).get_tex_string())

                comp = TextMobject(f"{val1} < {val2}")
                comp.next_to(nodes_grp, UP)

                self.play(ApplyMethod(sqr1.set_fill, YELLOW),
                             ApplyMethod(sqr2.set_fill, YELLOW))
                self.play(Write(comp))

                if val1 < val2:
                    swaps_made = True
                    self.play(CyclicReplace(nodes[i], nodes[j]))
                    temp = nodes[i]
                    nodes[i] = nodes[j]
                    nodes[j] = temp

                self.play(FadeOut(comp),
                            ApplyMethod(sqr1.set_fill, WHITE),
                            ApplyMethod(sqr2.set_fill, WHITE))

        self.wait(3)
