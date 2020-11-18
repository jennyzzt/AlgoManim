from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoaction import AlgoTransform, AlgoSceneAction
from algomanim.metadata import LowerMetadata, attach_metadata
from algomanim.algoobject import AlgoObject

class AlgoLinkedListNode(AlgoNode):
    def __init__(self, scene, val, next_node=None):
        self.arrow = Arrow(ORIGIN, ORIGIN, stroke_width=5, color=WHITE)
        self.next_node = next_node

        super().__init__(scene, val)

    def set_arrow_start_end(self):
        if self.next_node is None:
            self.arrow.set_opacity(0)
        else:
            start = self.grp.get_right()
            end = self.next_node.grp.get_left()
            self.arrow.put_start_and_end_on(start, end)

    @attach_metadata
    def show(self, metadata=None, animated=True, w_prev=False):
        if self.next_node is not None:
            action = AlgoSceneAction.create_static_action(self.set_arrow_start_end)
            set_arrow_pair = self.scene.add_action_pair(action, action, animated=False)

            anim_action = self.scene.create_play_action(AlgoTransform(FadeIn(self.arrow)),
                w_prev=w_prev)
            static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.arrow])
            animate_arrow_pair = self.scene.add_action_pair(anim_action, static_action,
                animated=animated)

            # Add Metadata for GUI
            set_arrow_metadata = LowerMetadata.create(set_arrow_pair)
            animate_arrow_metadata = LowerMetadata.create(animate_arrow_pair)
            metadata.add_lower(set_arrow_metadata)
            metadata.add_lower(animate_arrow_metadata)
        super().show(metadata=metadata, animated=animated, w_prev=True)

class AlgoLinkedList(AlgoObject):
    def __init__(self, scene, arr, show=True):
        super().__init__(scene)

        # Make and arrange nodes
        self.nodes = []
        for val in arr:
            curr_node = AlgoLinkedListNode(scene, val)
            if len(self.nodes) != 0:
                self.nodes[-1].next_node = curr_node
            self.nodes.append(curr_node)

        for i in range(1, len(self.nodes)):
            self.nodes[i].grp.next_to(self.nodes[i - 1].grp, 3 * RIGHT)

        self.grp = VGroup(*[n.grp for n in self.nodes])

        # Initial positioning
        self.center(animated=False)

        if show:
            # Show all nodes in the list
            for node in self.nodes:
                node.show(animated=True)
