from manimlib.imports import *
from algomanim.algoaction import AlgoTransform, AlgoSceneAction
from algomanim.metadata import LowerMetadata, attach_metadata
from algomanim.settings import Shape
from algomanim.algoobject import AlgoObject

class AlgoNode(AlgoObject):
    def __init__(self, scene, val):
        super().__init__(scene)
        self.scene = scene

        # Get preconfig settings
        self.node_color = scene.settings['node_color']
        self.highlight_color = scene.settings['highlight_color']
        node_size = float(scene.settings['node_size'])
        self.node_length = node_size
        self.node = {
            Shape.CIRCLE: Circle(
                color=self.node_color,
                fill_opacity=1,
                radius=self.node_length / 2,
            ),
            Shape.SQUARE: Square(
                fill_color=self.node_color,
                fill_opacity=1,
                side_length=self.node_length
            ),
            Shape.SQUIRCLE: RoundedRectangle(
                height=self.node_length,
                width=self.node_length,
                fill_color=self.node_color,
                fill_opacity=1
            )
        }[scene.settings['node_shape']]

        # Set attributes
        self.val = val
        self.txt = self.generate_text(val)
        self.grp = VGroup(self.node, self.txt)

    def generate_text(self, val):
        text = TextMobject(str(val))
        text.scale(self.node_length * 1.5)
        text.set_color(self.scene.settings['font_color'])
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
