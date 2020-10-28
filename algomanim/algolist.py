# pylint: disable=E0602,E1101,R0903
from enum import Enum, auto
from collections import Counter
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
    SET_RIGHT_OF = auto()

class Metadata:
    counter = Counter()

    def __init__(self, metadata):
        self.metadata = metadata
        Metadata.counter[metadata] += 1

        self.fid = Metadata.counter[metadata]
        self.children = []

    def add_lower(self, lowermeta):
        self.children.append(lowermeta)

    def get_all_action_pairs(self):
        return list(map(lambda lower: lower.action_pair, self.children))

    def __str__(self):
        return f'Metadata(meta={self.metadata}, fid={self.fid}' + \
                                    f', children=[{self.__print_children()}])'

    def __print_children(self):
        strings = []
        for i in self.children:
            strings.append(str(i) + ', ')

        return ''.join(strings)

class LowerMetadata:

    def __init__(self, metadata, action_pair, val=None):
        if val is None:
            val = []
        self.metadata = metadata
        self.action_pair = action_pair
        self.val = val  # list of values affected by function

    def __str__(self):
        return f'LowerMetadata(meta={self.metadata}, val={self.val}' + \
                                        f', action_pair={self.action_pair})'

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
        self.scene.add_action_pair(action, action, animated=False)

        # Only add to meta_trees if it comes from a high-level function and not initialisation
        if metadata:
            # Initialise a LowerMetadata class for this low level function
            action_pair = self.scene.action_pairs[-1]
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
            AlgoTransform([node.grp, self.grp], transform=CyclicReplace),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.static_swap, AlgoTransform([node]))

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
        lower_meta = LowerMetadata(AlgoListMetadata.SWAP, action_pair, val=[self.val, node.val])

        assert metadata is not None
        metadata.add_lower(lower_meta)

    def show(self, metadata, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.add, AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
        lower_meta = LowerMetadata(AlgoListMetadata.SHOW, action_pair, val=[self.val])

        metadata.add_lower(lower_meta)

    def hide(self, metadata, animated=True, w_prev=False):
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp], transform=FadeOut),
            w_prev=w_prev
        )
        static_action = AlgoSceneAction(self.scene.remove,
            AlgoTransform([self.grp]), w_prev=w_prev)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
        lower_meta = LowerMetadata(AlgoListMetadata.SHOW, action_pair, val=[self.val, node.val])

        metadata.add_lower(lower_meta)

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

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
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
        static_action = AlgoSceneAction(
            self.node.set_fill,
            AlgoTransform([self.node_color], color_index=0)
        )

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
        lower_meta = LowerMetadata(AlgoListMetadata.DEHIGHLIGHT, action_pair, val=[self.val])

        assert metadata is not None
        metadata.add_lower(lower_meta)


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
        metadata = Metadata(AlgoListMetadata.SWAP)

        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], animated, metadata=metadata)

        self.scene.add_metadata(metadata)

    def compare(self, i, j, animated=True):
        meta = Metadata(AlgoListMetadata.COMPARE)
        self.dehighlight(*list(range(len(self.nodes))), animated=animated, metadata=meta)
        self.highlight(i, j, animated=animated, metadata=meta)

        self.scene.add_metadata(meta)

        return self.get_val(i, metadata=meta) < self.get_val(j, metadata=meta)

    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    def center(self, animated=True, metadata=None):
        curr_metadata = metadata if metadata else Metadata(AlgoListMetadata.CENTER)

        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction(self.grp.center)

        self.scene.add_action_pair(anim_action, static_action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        action_pair = self.scene.action_pairs[-1]
        lower_meta = LowerMetadata(AlgoListMetadata.CENTER, action_pair)

        curr_metadata.add_lower(lower_meta)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(curr_metadata)

    def show(self, animated=True):
        meta = Metadata(AlgoListMetadata.SHOW)
        for node in self.nodes:
            node.show(meta, animated)

        self.scene.add_metadata(meta)

    def hide(self, animated=True):
        meta = Metadata(AlgoListMetadata.HIDE)
        for node in self.nodes:
            node.hide(meta, animated)

        self.scene.add_metadata(meta)

    def highlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.HIGHLIGHT)
        for index in indexes:
            if first:
                self.nodes[index].highlight(animated, metadata=cur_metadata)
                first = False
            else:
                self.nodes[index].highlight(animated, w_prev=True, metadata=cur_metadata)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(cur_metadata)

    def dehighlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.DEHIGHLIGHT)
        for index in indexes:
            if first:
                self.nodes[index].dehighlight(animated, metadata=cur_metadata)
                first = False
            else:
                self.nodes[index].dehighlight(animated, w_prev=True, metadata=cur_metadata)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(cur_metadata)

    def get_val(self, index, animated=False, metadata=None):
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.GET_VAL)
        if animated:
            self.highlight(index, metadata=metadata)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(cur_metadata)

        return self.nodes[index].val

    def len(self):
        return len(self.nodes)

    def append(self, val, animated=True):
        node = AlgoListNode(self.scene, val)
        meta = Metadata(AlgoListMetadata.APPEND)
        if self.len() > 0:
            node.set_right_of(self.nodes[-1], metadata=meta)
        self.nodes.append(node)

        node.show(meta, animated)
        self.group()
        self.center(animated=False, metadata=meta)

        self.scene.add_metadata(meta)

    # List type functions: needs refactored to fit meta_trees / Metadata functionality
    # Currently not needed for Iteration3's bubblesort
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

            self.scene.add_action_pair(anim_action, static_action, animated=animated)

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
        self.scene.add_action_pair(anim_action, static_action, animated=animated)
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

        self.scene.add_action_pair(anim_action, static_action, animated=animated)
        self.group()

    @staticmethod
    def find_action_pairs(scene, occurence, method, lower_level=None):
        for meta_tree in scene.meta_trees:
            if method == meta_tree.metadata and occurence == meta_tree.fid:
                if lower_level:
                    pairs = []
                    for lower in meta_tree.children:
                        if lower_level == lower.metadata:
                            pairs.append(lower.action_pair)
                    return pairs
                return meta_tree.get_all_action_pairs()
        return []
