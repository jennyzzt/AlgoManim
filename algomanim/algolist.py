# pylint: disable=E0602,E1101,R0903
from enum import Enum, auto
from manimlib.imports import *
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.settings import Shape

class AlgoListMetadata(Enum):
    SWAP = auto()
    COMPARE = auto()
    CENTER = auto()
    SHOW = auto()
    HIDE = auto()
    HIGHLIGHT = auto()
    DEHIGHLIGHT = auto()
    GET_VAL = auto()
    APPEND = auto()
    POP = auto()
    SLICE = auto()
    CONCAT = auto()

class Metadata:
    global_uid = 0
    def __init__(self, metadata):
        self.metadata = metadata
        self.uid = Metadata.global_uid
        Metadata.global_uid += 1

class AlgoListNode:
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
        action = AlgoSceneAction(self.grp.next_to, AlgoTransform([node.grp, RIGHT]))
        self.scene.add_action_pair(action, action, animated=False, metadata=metadata)

    def show(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.add, AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=metadata)

    def hide(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.remove,
            AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=metadata)

    def highlight(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.node.set_fill, self.highlight_color],
                          transform=ApplyMethod, color_index=1),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(
            self.node.set_fill,
            AlgoTransform([self.highlight_color], color_index=0)
        )

        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=metadata)

    def dehighlight(self, animated=True, w_prev=False, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [self.node.set_fill, self.node_color],
                transform=ApplyMethod,
                color_index=1
            ),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(
            self.node.set_fill,
            AlgoTransform([self.node_color], color_index=0)
        )

        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=metadata)

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

        static_action = AlgoSceneAction(self.static_swap, AlgoTransform([node]), w_prev=w_prev)
        static_action2 = AlgoSceneAction(lambda x: x, AlgoTransform([1]), w_prev=True)

        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=metadata)
        self.scene.add_action_pair(anim_action2, static_action2, animated=animated,
            metadata=metadata)

class AlgoList:
    def __init__(self, scene, arr):
        # make nodes
        self.scene = scene
        self.nodes = [AlgoListNode(scene, val) for val in arr]

        # arrange nodes in order
        for i in range(1, len(self.nodes)):
            self.nodes[i].set_right_of(self.nodes[i - 1])

        # group nodes together
        self.group()
        self.center(animated=False)
        self.show(animated=False)

    def swap(self, i, j, animated=True):
        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], animated, metadata=Metadata(AlgoListMetadata.SWAP))

    def compare(self, i, j, animated=True):
        meta = Metadata(AlgoListMetadata.COMPARE)
        self.dehighlight(*list(range(len(self.nodes))), animated=animated, metadata=meta)
        self.highlight(i, j, animated=animated, metadata=meta)
        return self.get_val(i) < self.get_val(j)

    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    def center(self, animated=True, metadata=None):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction(self.grp.center)

        self.scene.add_action_pair(anim_action, static_action, animated=animated,
            metadata=metadata if metadata else Metadata(AlgoListMetadata.CENTER))

    def show(self, animated=True):
        meta = Metadata(AlgoListMetadata.SHOW)
        for node in self.nodes:
            node.show(animated, metadata=meta)

    def hide(self, animated=True):
        meta = Metadata(AlgoListMetadata.HIDE)
        for node in self.nodes:
            node.hide(animated, metadata=meta)

    def highlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.HIGHLIGHT)
        for index in indexes:
            if first:
                self.nodes[index].highlight(animated, metadata=cur_metadata)
                first = False
            else:
                self.nodes[index].highlight(animated, w_prev=True, metadata=cur_metadata)

    def dehighlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.DEHIGHLIGHT)
        for index in indexes:
            if first:
                self.nodes[index].dehighlight(animated, metadata=cur_metadata)
                first = False
            else:
                self.nodes[index].dehighlight(animated, w_prev=True, metadata=cur_metadata)

    def get_val(self, index, animated=False):
        if animated:
            self.highlight(index, metadata=Metadata(AlgoListMetadata.GET_VAL))
        return self.nodes[index].val

    def len(self):
        return len(self.nodes)

    def append(self, val, animated=True):
        node = AlgoListNode(self.scene, val)
        meta = Metadata(AlgoListMetadata.APPEND)
        if self.len() > 0:
            node.set_right_of(self.nodes[-1], metadata=meta)
        self.nodes.append(node)

        node.show(animated, metadata=meta)
        self.group()
        self.center(animated=False, metadata=meta)

    def pop(self, i=None, animated=True):
        if i is None:
            i = self.len()-1
        elif i < 0 or i >= self.len():
            return
        left_node = self.nodes[i - 1] if i != 0 else None
        right_nodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        self.nodes[i].hide(animated)
        self.nodes.remove(self.nodes[i])
        self.group()

        if right_nodes is not None and left_node is not None:
            # gap only needs to be closed if there are nodes on the left and right
            # if not, simply centering the remaining list would be enough
            right_grp = VGroup(*[node.grp for node in right_nodes])

            anim_action = self.scene.create_play_action(
                AlgoTransform([right_grp.next_to, left_node.grp, RIGHT], transform=ApplyMethod)
            )
            static_action = AlgoSceneAction(right_grp.set_right_of, AlgoTransform([left_node]))

            self.scene.add_action_pair(anim_action, static_action, animated=animated,
                                        metadata=Metadata(AlgoListMetadata.POP))

    def slice(self, start, stop, step=1, animated=True):
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()

        meta = Metadata(AlgoListMetadata.SLICE)
        self.highlight(*range(start, stop, step), animated=animated, metadata=meta)

        subvals = [n.val for n in self.nodes][start:stop:step]
        sublist = AlgoList(self.scene, subvals)

        action = AlgoSceneAction(sublist.grp.align_to, *[self.nodes[start].grp, LEFT])
        self.scene.add_action_pair(action, action, animated=animated, metadata=meta)

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [sublist.grp.shift, DOWN * 1.1 * self.nodes[0].node_length],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction(sublist.grp.shift,
            AlgoTransform([DOWN * 1.1 * self.nodes[0].node_length]))
        self.scene.add_action_pair(anim_action, static_action, animated=animated, metadata=meta)
        return sublist

    def concat(self, other_list, animated=True):
        self.nodes += other_list.nodes

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [other_list.grp.next_to, self.grp, RIGHT],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction(other_list.grp.next_to, AlgoTransform([self.grp, RIGHT]))

        self.scene.add_action_pair(anim_action, static_action, animated=animated,
                                        metadata=Metadata(AlgoListMetadata.CONCAT))
        self.group()

    @staticmethod
    def find_index(action_pairs, method, occurence):
        indexes = []
        uids = set()
        for i, action_pair in enumerate(action_pairs):
            meta = action_pair.metadata
            if meta is None:
                continue

            if len(uids) <= occurence:
                if meta.metadata == method:
                    if meta.uid not in uids:
                        uids.add(meta.uid)
                    if len(uids) == occurence:
                        indexes.append(i)
            else:
                break

        return indexes
