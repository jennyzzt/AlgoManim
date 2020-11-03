from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import LowerMetadata, AlgoListMetadata
from algomanim.shape import Shape

class AlgoNode:
    def __init__(self, scene, val):
        self.scene = scene
        self.node_color = scene.settings['node_color']
        self.highlight_color = scene.settings['highlight_color']
        self.node_length = scene.settings['node_size']
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
        self.val = val
        self.txt = TextMobject(str(val))
        self.txt.set_color(scene.settings['font_color'])

        self.grp = VGroup(self.node, self.txt)

    def set_right_of(self, node, metadata=None):
        action = AlgoSceneAction.create_static_action(self.grp.next_to, [node.grp, RIGHT])
        action_pair = self.scene.add_action_pair(action, action, animated=False)

        # Only add to meta_trees if it comes from a high-level function and not initialisation
        if metadata:
            # Initialise a LowerMetadata class for this low level function
            lower_meta = LowerMetadata(AlgoListMetadata.SET_RIGHT_OF,
                                            action_pair, val=[self.val, node.val])

            metadata.add_lower(lower_meta)

    def static_swap(self, node):
        self_center = self.grp.get_center()
        node_center = node.grp.get_center()
        self.grp.move_to(node_center)
        node.grp.move_to(self_center)

    def swap_with(self, node, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp, node.grp], transform=CyclicReplace),
            w_prev=w_prev
        )
        anim_action2 = self.scene.create_play_action(
            AlgoTransform([node.grp, self.grp], transform=CyclicReplace),
            w_prev=True
        )

        static_action = AlgoSceneAction.create_static_action(self.static_swap, [node])
        static_action2 = AlgoSceneAction.create_empty_action()

        action_pair1 = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        action_pair2 = self.scene.add_action_pair(anim_action2, static_action2, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta1 = LowerMetadata(AlgoListMetadata.SWAP, action_pair1, val=[self.val, node.val])
        lower_meta2 = LowerMetadata(AlgoListMetadata.SWAP, action_pair2, val=[node.val, self.val])

        assert metadata is not None
        metadata.add_lower(lower_meta1)
        metadata.add_lower(lower_meta2)

    def show(self, metadata, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.grp])

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta = LowerMetadata(AlgoListMetadata.SHOW, action_pair, val=[self.val])

        metadata.add_lower(lower_meta)

    def hide(self, metadata, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.remove, [self.grp])

        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta = LowerMetadata(AlgoListMetadata.SHOW, action_pair, val=[self.val])

        metadata.add_lower(lower_meta)

    def highlight(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.node.set_fill, self.highlight_color],
                          transform=ApplyMethod, color_index=1),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(
            self.node.set_fill,
            [self.highlight_color],
            color_index=0
        )

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta = LowerMetadata(AlgoListMetadata.HIGHLIGHT, action_pair, val=[self.val])

        assert metadata is not None
        metadata.add_lower(lower_meta)

    def dehighlight(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [self.node.set_fill, self.node_color],
                transform=ApplyMethod,
                color_index=1
            ),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(
            self.node.set_fill,
            [self.node_color],
            color_index=0
        )

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta = LowerMetadata(AlgoListMetadata.DEHIGHLIGHT, action_pair, val=[self.val])
        assert metadata is not None
        metadata.add_lower(lower_meta)
