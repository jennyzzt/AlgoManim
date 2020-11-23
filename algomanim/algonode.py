import numpy as np
from manimlib.imports import *
from algomanim.algoaction import AlgoTransform, AlgoSceneAction
from algomanim.metadata import LowerMetadata, attach_metadata
from algomanim.algoobject import AlgoObject

class AlgoNode(AlgoObject):
    def __init__(self, scene, val):
        super().__init__(scene)
        self.scene = scene

        # Use preconfig settings to determine node configuration
        self.node_color = scene.settings['node_color']
        self.highlight_color = scene.settings['highlight_color']
        node_size = float(scene.settings['node_size'])
        self.node_length = node_size
        nodes = {
            'circle': Circle(
                color=self.node_color,
                fill_opacity=1,
                radius=self.node_length / 2,
            ),
            'square': Square(
                fill_color=self.node_color,
                fill_opacity=1,
                side_length=self.node_length
            ),
            'squircle': RoundedRectangle(
                height=self.node_length,
                width=self.node_length,
                fill_color=self.node_color,
                fill_opacity=1
            )
        }
        try:
            self.node = nodes[scene.settings['node_shape'].lower()]
        except KeyError:
            print("Unrecognized node shape, defaulting to Square")
            self.node = nodes['square']

        # Set attributes
        self.lines = {}
        self.val = val
        self.txt = self.generate_text(val)
        self.grp = VGroup(self.node, self.txt)

    def generate_text(self, val):
        text = self.scene.create_text(str(val), for_node=True)
        text.scale(self.node_length * 1.5)
        return text

    def static_replace_text(self, old_text, new_text):
        new_text.move_to(old_text.get_center())
        self.scene.remove(old_text)
        self.scene.add(new_text)

    @staticmethod
    def animated_replace_text(old_text, new_text):
        new_text.move_to(old_text.get_center())
        return [FadeOut(old_text), ReplacementTransform(old_text, new_text)]

    @attach_metadata
    def change_value(self, val, metadata=None, animated=True, w_prev=False):
        old_text = self.txt
        new_text = self.generate_text(val)
        new_text.move_to(self.txt.get_center())
        self.val = val
        self.txt = new_text
        self.grp = VGroup(self.node, self.txt)

        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([old_text, new_text],
                transform=self.animated_replace_text
            ),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(
            self.static_replace_text, [old_text, new_text]
        )
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        metadata.add_lower(lower_meta)

    @attach_metadata
    def highlight(self, metadata=None, animated=True, w_prev=False):
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.node.set_fill, self.highlight_color], transform=ApplyMethod,
                          color_index=1), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(
            self.node.set_fill, [self.highlight_color], color_index=0
        )
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        metadata.add_lower(lower_meta)

    @attach_metadata
    def dehighlight(self, metadata=None, animated=True, w_prev=False):
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.node.set_fill, self.node_color], transform=ApplyMethod,
                          color_index=1), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(
            self.node.set_fill, [self.node_color], color_index=0
        )
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        metadata.add_lower(lower_meta)

    @attach_metadata
    def add_line(self, target_node, weight=None, **kwargs):
        metadata = kwargs["metadata"] if "metadata" in kwargs else None
        animated = kwargs["animated"] if "animated" in kwargs else True
        w_prev = kwargs["w_prev"] if "w_prev" in kwargs else False

        if target_node in self.lines:
            line, old_weight = self.lines[target_node]
            weight_obj = TextMobject(str(weight)) if weight else old_weight
        else:
            line = Line(ORIGIN, ORIGIN, stroke_width=self.scene.settings['line_width'],
                                            color=self.scene.settings['line_color'])
            weight_obj =  TextMobject(str(weight)) if weight else None
            self.lines[target_node] = line, weight_obj
            target_node.lines[self] = line, weight_obj

        # Set the start and end points of the line from current node to target node
        action = AlgoSceneAction.create_static_action(self.set_line_start_end,
                                                                    [target_node])
        action_pair = self.scene.add_action_pair(action, action, animated=False)

        lower_meta = LowerMetadata.create(action_pair, [self.val], False)
        metadata.add_lower(lower_meta)

        # Fade in the line
        anim_action = self.scene.create_play_action(AlgoTransform(FadeIn(line)),
                                                                    w_prev=w_prev)
        static_action = AlgoSceneAction.create_static_action(self.scene.add,
                                                                    [line])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

        lower_meta = LowerMetadata.create(action_pair, [self.val])
        metadata.add_lower(lower_meta)

        if weight_obj:
            # Position Text for Line Weight
            action = AlgoSceneAction.create_static_action(self.weight_placement,
                                                                        [weight_obj, line])
            action_pair = self.scene.add_action_pair(action, action, animated=False)

            lower_meta = LowerMetadata.create(action_pair, [weight_obj.get_tex_string()], False)
            metadata.add_lower(lower_meta)

            # Add Text for Line Weight
            anim_action = self.scene.create_play_action(AlgoTransform(Write(weight_obj)),
                                                                        w_prev=w_prev)
            static_action = AlgoSceneAction.create_static_action(self.scene.add,
                                                                        [weight_obj])
            action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

            lower_meta = LowerMetadata.create(action_pair, [weight_obj.get_tex_string()])
            metadata.add_lower(lower_meta)

    def weight_placement(self, weight, line):
        angle = line.get_angle() + np.pi/2
        weight.move_to(line.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) / 3)

    def set_line_start_end(self, target):
        if target is None:
            # reset line
            self.lines[target][0].set_opacity(0)
        else:
            center = self.grp.get_center()
            target_center = target.grp.get_center()
            pos_y = center[1] - target_center[1]
            pos_x = center[0] - target_center[0]
            angle = np.arctan2(pos_y, pos_x)
            start = center - \
                self.scene.settings['node_size'] / 2 * np.array([np.cos(angle), np.sin(angle), 0])
            end = target_center + \
                self.scene.settings['node_size'] / 2 * np.array([np.cos(angle), np.sin(angle), 0])
            self.lines[target][0].put_start_and_end_on(start, end)
