from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata
from algomanim.settings import Shape
from algomanim.algoobject import AlgoObject

class AlgoNode(AlgoObject):
    def __init__(self, scene, val):
        super().__init__(scene)
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
        self.txt = TextMobject(str(val))
        self.txt.scale(node_size * 1.5)
        self.txt.set_color(scene.settings['font_color'])
        self.grp = VGroup(self.node, self.txt)

    def highlight(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
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
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    def dehighlight(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
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
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)
