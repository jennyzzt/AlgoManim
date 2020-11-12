#!/usr/bin/env python
# pylint: disable=E0602

from manimlib.imports import *

class BubbleSortScene(Scene):
    def init_list(self, input_list):
        nodes = []

        for i in input_list:
            node = Circle(          # Square to Circle
                color=WHITE,        # fill_color to color
                fill_opacity=1,
                radius=1.2          #side_length to radius
            )
            txt = TextMobject(str(i))
            txt.set_color(BLACK)
            grp = VGroup(node, txt)
            nodes.append(grp)

        for i in range(1, len(nodes)):
            nodes[i].next_to(nodes[i - 1], RIGHT)

        for node in nodes:
            self.add(node)

        nodes_grp = VGroup(*nodes)
        self.play(nodes_grp.center)
        return nodes, nodes_grp

    def construct(self):
        input_list = [25, 43, 5, 18, 30]
        nodes, nodes_grp = self.init_list(input_list)

        fade_on_compare = 10
        swaps_made = True
        compare = 0

        while swaps_made:
            swaps_made = False
            for i in range(len(nodes) - 1):
                j = i + 1
                compare += 1
                highlight_color = '#33cccc'

                node1 = nodes[i].__getitem__(0)
                node2 = nodes[j].__getitem__(0)
                val1 = int(nodes[i].__getitem__(1).get_tex_string())
                val2 = int(nodes[j].__getitem__(1).get_tex_string())

                comp = TextMobject(f"{val1} < {val2}")
                comp.next_to(nodes_grp, UP)

                if compare == 1:
                    highlight_color = '#ff6666'

                if compare == fade_on_compare:
                    self.play(FadeOut(nodes_grp))

                if compare < fade_on_compare:
                    self.play(ApplyMethod(node1.set_fill, highlight_color),
                                ApplyMethod(node2.set_fill, highlight_color),
                                Write(comp))

                if val1 < val2:
                    swaps_made = True
                    if compare < fade_on_compare:
                        self.play(CyclicReplace(nodes[i], nodes[j], run_time=0.5))
                    temp = nodes[i]
                    nodes[i] = nodes[j]
                    nodes[j] = temp

                if compare < fade_on_compare:
                    self.play(FadeOut(comp),
                            ApplyMethod(node1.set_fill, WHITE),
                            ApplyMethod(node2.set_fill, WHITE))
        self.play(FadeIn(nodes_grp))
        self.wait(3)
