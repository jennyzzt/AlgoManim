#!/usr/bin/env python

from manimlib.imports import *

# To watch one of these scenes, run the following:
# python -m manim example_scenes.py SquareToCircle -pl
#
# Use the flat -l for a faster rendering at a lower
# quality.
# Use -s to skip to the end and just save the final frame
# Use the -p to have the animation (or image, if -s was
# used) pop up once done.
# Use -n <number> to skip ahead to the n'th animation of a scene.
# Use -r <number> to specify a resolution (for example, -r 1080
# for a 1920x1080 video)


class BubbleSortManimScene(Scene):
    def construct(self):
        input_list = [25, 43, 5, 18, 30]
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

        swaps_made = True

        while swaps_made:
            swaps_made = False
            for i in range(len(nodes) - 1):
                j = i + 1

                sqr1 = nodes[i].__getitem__(0)
                sqr2 = nodes[j].__getitem__(0)
                txt1 = nodes[i].__getitem__(1)
                txt2 = nodes[j].__getitem__(1)
                val1 = int(txt1.get_tex_string())
                val2 = int(txt2.get_tex_string())

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
