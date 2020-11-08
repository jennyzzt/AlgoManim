# pylint: disable=E1101
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata


class AlgoList:
    def __init__(self, scene, arr, show=True):
        # Make nodes
        self.scene = scene
        self.nodes = [AlgoNode(scene, val) for val in arr]

        # Arrange nodes in order
        for i in range(1, len(self.nodes)):
            self.nodes[i].grp.next_to(self.nodes[i - 1].grp, RIGHT)

        # Group nodes together
        self.grp = None
        self.group()

        self.grp.center()
        # self.center(animated=False)

        if show:
            self.show(animated=False)

        # Subscribe to the scene for scene transformations like Shifts
        scene.track_algoitem(self)

    # Swaps the nodes at indexes i and j
    def swap(self, i, j, animated=True):
        metadata = Metadata.create_fn_metadata()

        # swap nodes
        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], animated, metadata=metadata)

        self.scene.add_metadata(metadata)

    def compare(self, i, j, animated=True, highlights=True):
        meta = Metadata.create_fn_metadata()
        if highlights:
            self.dehighlight(*list(range(len(self.nodes))), animated=animated, metadata=meta)
            self.highlight(i, j, animated=animated, metadata=meta)

        self.scene.add_metadata(meta)
        return self.get_val(i) < self.get_val(j)

    # Restores the internal VGroup of list nodes
    # especially if the list has been edited
    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    # Centre the list on screen
    def center(self, animated=True, metadata=None):
        curr_metadata = metadata if metadata else Metadata.create_fn_metadata()

        anim_action = self.scene.create_play_action(
            AlgoTransform([self.grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction.create_static_action(self.grp.center)

        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Create LowerMetadata
        lower_meta = LowerMetadata('center', action_pair)
        curr_metadata.add_lower(lower_meta)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(curr_metadata)

    # Display the list on screen
    def show(self, animated=True):
        meta = Metadata.create_fn_metadata()
        for node in self.nodes:
            node.show(meta, animated)

        self.scene.add_metadata(meta)

    # Hide the list on screen
    def hide(self, animated=True, metadata=None):
        cur_metadata = metadata if metadata else Metadata.create_fn_metadata()

        for node in self.nodes:
            node.hide(cur_metadata, animated)

        if metadata is None:
            self.scene.add_metadata(cur_metadata)

    # Highlight nodes at the specified indexes
    def highlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata.create_fn_metadata()
        for index in indexes:
            if first:
                # first node should not be highlighted together with the previous action
                self.nodes[index].highlight(animated, metadata=cur_metadata)
                first = False
            else:
                # subsequent nodes should be highlighted together with the first highlight
                self.nodes[index].highlight(animated, w_prev=True, metadata=cur_metadata)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(cur_metadata)

    # Unhighlight nodes at the specified indexes
    def dehighlight(self, *indexes, animated=True, metadata=None):
        first = True
        cur_metadata = metadata if metadata else Metadata.create_fn_metadata()
        for index in indexes:
            if first:
                # first node should not be dehighlighted together with the previous action
                self.nodes[index].dehighlight(animated, metadata=cur_metadata)
                first = False
            else:
                # subsequent nodes should be highlighted together with the first dehighlight
                self.nodes[index].dehighlight(animated, w_prev=True, metadata=cur_metadata)

        # Only add if it is a higher level function
        if metadata is None:
            self.scene.add_metadata(cur_metadata)

    def get_val(self, index):
        return self.nodes[index].val

    # Returns the length of the list
    def len(self):
        return len(self.nodes)

    # Appends a new node with the given value to the end of the list
    def append(self, val, animated=True):
        node = AlgoNode(self.scene, val)
        meta = Metadata.create_fn_metadata()
        if self.len() > 0:
            node.set_right_of(self.nodes[-1], metadata=meta)
        self.nodes.append(node)

        node.show(meta, animated)
        self.group()
        self.center(animated=animated, metadata=meta)

        self.scene.add_metadata(meta)

    # List type functions: needs refactored to fit meta_trees / Metadata functionality
    # Currently not needed for Iteration3's bubblesort

    # Removes the node at the specified index and closes the gap in the list if necessary
    # If no index is specified, removes the last node by default
    def pop(self, i=None, animated=True):
        if i is None:
            i = self.len()-1
        elif i < 0 or i >= self.len():
            return
        left_node = self.nodes[i - 1] if i != 0 else None
        right_nodes = self.nodes[i + 1:] if i != len(self.nodes) - 1 else None

        meta = Metadata.create_fn_metadata()

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
            lower_meta = LowerMetadata('temp', action_pair)
            meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

    @staticmethod
    def align_nodes_from_first_node(algolist):
        for i in range(1, algolist.len()):
            algolist.nodes[i].grp.next_to(algolist.nodes[i - 1].grp, RIGHT)

    @staticmethod
    def align_nodes_from_last_node(algolist):
        for i in reversed(range(0, algolist.len() - 1)):
            algolist.nodes[i].grp.next_to(algolist.nodes[i + 1].grp, LEFT)

    # enforced contiguous slices
    # move = LEFT or RIGHT, denoting which direction the slice should be shifted in
    def slice(self, start, stop, move=LEFT, animated=True):
        # Fix indices if needed
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()

        meta = Metadata.create_fn_metadata()

        # Highlight the sublist we want to keep
        self.highlight(*range(start, stop), animated=animated, metadata=meta)

        # Dehighlight the sublist we want to keep
        self.dehighlight(*range(start, stop), animated=animated, metadata=meta)

        """
        The sliced list is first aligned to its original position in the list.
        The hidden list is positioned where the sliced list will end up,
        and its center is used to define the movement of the sliced list.
        
        Both slices are hidden from the screen during this process.
        """

        # Shift the Scene up so that that we make space for the new list
        self.scene.shift_scene(UP)

        # Create sliced list in background
        sublist = AlgoList(self.scene,
                           [n.val for n in self.nodes][start:stop], show=False)

        # Align to its original position in the list
        sublist.nodes[0].grp.align_to(self.nodes[start].grp, LEFT)
        AlgoList.align_nodes_from_first_node(sublist)

        hidden_sublist = AlgoList(self.scene,
                                  [n.val for n in self.nodes][start:stop], show=False)

        # Position hidden sliced list by taking reference from last element
        hidden_sublist.nodes[-1].grp.next_to(self.nodes[stop - 1].grp, DOWN + move)
        AlgoList.align_nodes_from_last_node(hidden_sublist)

        move_pt = hidden_sublist.grp.get_center()

        # Shift sublist to position of hidden_sublist
        anim_action = self.scene.create_play_action(
            AlgoTransform(
                [sublist.grp.move_to, move_pt],
                transform=ApplyMethod
            )
        )
        static_action = AlgoSceneAction.create_static_action(
            sublist.grp.move_to,
            [move_pt]
        )
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)

        lower_meta = LowerMetadata('temp', action_pair)
        meta.add_lower(lower_meta)

        # Get rid of hidden_sublist
        self.scene.remove(hidden_sublist)

        # Add metadata to scene
        self.scene.add_metadata(meta)

        return sublist

    # Concatenates this list and other_list, then centres them
    def concat(self, other_list, animated=True, center=False):
        # Join both lists in the backend
        self.nodes += other_list.nodes

        meta = Metadata.create_fn_metadata()

        # Join the two lists visually
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

        # Create LowerMetadata
        lower_meta = LowerMetadata('temp', action_pair)
        meta.add_lower(lower_meta)

        # Update the VGroup of list nodes
        self.group()

        if center:
            # Center the combined list
            anim_action = self.scene.create_play_action(
                AlgoTransform([self.grp.center], transform=ApplyMethod)
            )
            static_action = AlgoSceneAction.create_static_action(self.grp.center)
            action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                     animated=animated)

            # Create LowerMetadata
            lower_meta = LowerMetadata('center', action_pair)
            meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

        return self

    def shift_item(self, vector, animated=False, w_prev=False):
        for node in self.nodes:
            node.set_relative_of(node, vector, animated=animated, w_prev=w_prev)


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
