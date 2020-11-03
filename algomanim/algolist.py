# pylint: disable=E1101
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata, AlgoListMetadata
from copy import deepcopy

class AlgoList:
    def __init__(self, scene, arr):
        # make nodes
        self.scene = scene
        self.nodes = [AlgoNode(scene, val) for val in arr]

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
        static_action = AlgoSceneAction.create_static_action(self.grp.center)

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Initialise a LowerMetadata class for this low level function
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

    def hide(self, animated=True, metadata=None):
        cur_metadata = metadata if metadata else Metadata(AlgoListMetadata.HIDE)

        for node in self.nodes:
            node.hide(cur_metadata, animated)

        if metadata is None:
            self.scene.add_metadata(cur_metadata)

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
        node = AlgoNode(self.scene, val)
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

    # needs work on metadata
    def pop(self, i=None, animated=True):
        if i is None:
            i = self.len()-1
        elif i < 0 or i >= self.len():
            return
        left_node = self.nodes[i - 1] if i != 0 else None
        right_nodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        meta = Metadata(AlgoListMetadata.POP)

        self.nodes[i].hide(meta, animated)
        self.nodes.remove(self.nodes[i])
        self.group()

        if right_nodes is not None and left_node is not None:
            # gap only needs to be closed if there are nodes on the left and right
            # if not, simply centering the remaining list would be enough
            right_grp = VGroup(*[node.grp for node in right_nodes])

            anim_action = self.scene.create_play_action(
                AlgoTransform([right_grp.next_to, left_node.grp, RIGHT], transform=ApplyMethod)
            )
            static_action = AlgoSceneAction.create_static_action(
                right_grp.next_to,
                [left_node.grp, RIGHT]
            )

            action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

            # Initialise a LowerMetadata class for this low level function
            lower_meta = LowerMetadata(AlgoListMetadata.TEMP, action_pair)
            meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

    # metadata works but animation needs to be fixed
    def slice(self, start, stop, step=1, animated=True):
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()

        meta = Metadata(AlgoListMetadata.SLICE)

        # highlight the sublist we want to keep
        self.highlight(*range(start, stop, step), animated=animated, metadata=meta)

        # throw away the old values
        subvals = [n.val for n in self.nodes][start:stop:step]
        sublist = AlgoList(self.scene, subvals)

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [sublist.grp.align_to, self.nodes[start].grp, LEFT],
                transform=ApplyMethod
            )
        )
        action = AlgoSceneAction(sublist.grp.align_to, *[self.nodes[start].grp, LEFT])
        action_pair = self.scene.add_action_pair(anim_action, action, animated=animated)

        # Initialise a LowerMetadata class for this low level function
        lower_meta = LowerMetadata(AlgoListMetadata.TEMP, action_pair)
        meta.add_lower(lower_meta)

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [sublist.grp.shift, DOWN * 1.1 * self.nodes[0].node_length],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction.create_static_action(
            sublist.grp.shift,
            [DOWN * 1.1 * self.nodes[0].node_length]
        )
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        lower_meta = LowerMetadata(AlgoListMetadata.TEMP, action_pair)
        meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

        return sublist

    # needs work on metadata
    def concat(self, other_list, animated=True):
        self.nodes += other_list.nodes

        meta = Metadata(AlgoListMetadata.CONCAT)

        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [other_list.grp.next_to, self.grp, RIGHT],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction.create_static_action(
            other_list.grp.next_to,
            [self.grp, RIGHT]
        )

        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        lower_meta = LowerMetadata(AlgoListMetadata.TEMP, action_pair)
        meta.add_lower(lower_meta)

        # Center the combined list
        grp = VGroup(self.grp, other_list.grp)

        anim_action = self.scene.create_play_action(
            AlgoTransform([grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction.create_static_action(grp.center)
        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        lower_meta = LowerMetadata(AlgoListMetadata.CENTER, action_pair)
        meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

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
