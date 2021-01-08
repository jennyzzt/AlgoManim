from manimlib.imports import *

class FindMaxScene(Scene):
    def init_list(self, input_list):
        nodes = []

        for i in input_list:
            node = Circle(          # Square to Circle
                color=WHITE,        # fill_color to color
                fill_opacity=1,
                radius=0.5          #side_length to radius
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
        nodes_grp.center()
        return nodes, nodes_grp

    def construct(self):
        teal = '#33cccc'

        title = TextMobject("Find Maximum Value")
        title.shift(2 * UP)
        self.play(Write(title))

        input_list = [25, 40, 5, 60, 50, 80]
        nodes, _ = self.init_list(input_list)

        for (i, val) in enumerate(input_list):
            if i == 0:
                curr_max_id = 0
                curr_max_val = input_list[curr_max_id]
                new_title = TextMobject(f'Current Max Value: {curr_max_val}')
                new_title.shift(2 * UP)
                self.play(FadeOut(title), ReplacementTransform(title, new_title))
                title = new_title

                continue

            if val < curr_max_val:
                operator = '<='
            else:
                operator = '>'

            comp = TextMobject(f"{val} {operator} {curr_max_val}")
            comp.shift(UP)
            self.play(ApplyMethod(nodes[i].__getitem__(0).set_fill, teal),
                    ApplyMethod(nodes[curr_max_id].__getitem__(0).set_fill, teal), Write(comp))

            if operator == '>':
                new_title = TextMobject(f'Current Max Value: {val}')
                new_title.shift(2 * UP)
                self.play(FadeOut(title), ReplacementTransform(title, new_title))
                title = new_title

            self.play(ApplyMethod(nodes[i].__getitem__(0).set_fill, WHITE),
                    ApplyMethod(nodes[curr_max_id].__getitem__(0).set_fill, WHITE), FadeOut(comp))

            if operator == '>':
                curr_max_id = i
                curr_max_val = val
        self.wait(1)
