# pylint: disable=E1101, W0105, R0913
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata
from algomanim.algoobject import AlgoObject, TEMP_META_NAME


class AlgoList(AlgoObject):
    def __init__(self, scene, arr, show=True, displacement=None):
        super().__init__(scene)
        # Make and arrange nodes
        self.nodes = [AlgoNode(scene, val) for val in arr]
        self.displacement = ORIGIN if displacement is None else displacement
        if displacement is not None and len(self.nodes) > 0:
            self.nodes[0].grp.move_to(displacement)

        for i in range(1, len(self.nodes)):
            self.nodes[i].grp.next_to(self.nodes[i - 1].grp, RIGHT)

        # Group nodes together
        self.grp = None
        self.group(immediate_effect=True)

        # Initial positioning
        self.center(animated=False)

        # Subscribe to the scene for scene transformations like Shifts
        scene.track_algoitem(self)

        if show:
            self.show_list(animated=False)

    ''' Swaps the nodes at indexes i and j '''
    def swap(self, i, j, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # swap nodes
        temp = self.nodes[i]
        self.nodes[i] = self.nodes[j]
        self.nodes[j] = temp
        self.nodes[i].swap_with(self.nodes[j], metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Compare two nodes at indexes i and j '''
    def compare(self, i, j, metadata=None, animated=True, w_prev=False,
                highlights=True, text=True):
        meta = Metadata.check_and_create(metadata)
        if highlights:
            # Add highlight animations
            self.dehighlight(*list(range(len(self.nodes))),
                             metadata=meta, animated=animated, w_prev=w_prev)
            self.highlight(i, j, metadata=meta, animated=animated, w_prev=w_prev)
        # Get nodes' values
        val1 = self.get_val(i)
        val2 = self.get_val(j)
        if text:
            # Add associated text
            self.add_text(f"{str(val1)} < {str(val2)}", "compare", UP,
                          metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None and (highlights or text):
            self.scene.add_metadata(meta)
        return val1 < val2

    # Restores the internal VGroup of list nodes, especially if the list has been edited
    def group(self, metadata=None, immediate_effect=False):

        def group():
            self.grp = VGroup(*[n.grp for n in self.nodes])

        # Update the VGroup of the list
        if immediate_effect:
            group()
        else:

            dummy_action = AlgoSceneAction.create_static_action(group, [])
            dummy_action_pair = self.scene.add_action_pair(dummy_action,
                                                           dummy_action, animated=False)

            # Not designed to be a Higher level func
            if metadata:
                lower_meta = LowerMetadata.create(dummy_action_pair, [n.val for n in self.nodes])
                metadata.add_lower(lower_meta)

    ''' Display the list on screen '''
    def show_list(self, metadata=None, animated=True, w_prev=False):
        if len(self.nodes) > 0:
            meta = Metadata.check_and_create(metadata)
            # Show all nodes in the list
            for node in self.nodes:
                node.show(metadata=meta, animated=animated, w_prev=w_prev)
            # Add metadata if meta is created in this fn
            if metadata is None:
                self.scene.add_metadata(meta)

    ''' Hide the list from screen '''
    def hide_list(self, metadata=None, animated=True, w_prev=False):
        if len(self.nodes) > 0:
            meta = Metadata.check_and_create(metadata)
            # Hide all nodes in list
            for node in self.nodes:
                node.hide(metadata=meta, animated=animated, w_prev=w_prev)
            # Add metadata if meta is created in this fn
            if metadata is None:
                self.scene.add_metadata(meta)

    ''' Highlight nodes at the specified indexes '''
    def highlight(self, *indexes, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        first = True
        for index in indexes:
            if first:
                # first node should not be highlighted together with the previous action
                self.nodes[index].highlight(metadata=meta, animated=animated, w_prev=w_prev)
                first = False
            else:
                # subsequent nodes should be highlighted together with the first highlight
                self.nodes[index].highlight(metadata=meta, animated=animated, w_prev=True)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Dehighlight nodes at the specified indexes '''
    def dehighlight(self, *indexes, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        first = True
        for index in indexes:
            if first:
                # first node should not be dehighlighted together with the previous action
                self.nodes[index].dehighlight(metadata=meta, animated=animated, w_prev=w_prev)
                first = False
            else:
                # subsequent nodes should be highlighted together with the first dehighlight
                self.nodes[index].dehighlight(metadata=meta, animated=animated, w_prev=True)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Returns the value of the node at index
    def get_val(self, index):
        return self.nodes[index].val

    # Returns the length of the list
    def len(self):
        return len(self.nodes)

    ''' Appends a new node with the given value to the end of the list '''
    def append(self, val, metadata=None, animated=True, w_prev=False, center=True):
        meta = Metadata.check_and_create(metadata)
        # Create new node and add to the right of the list
        node = AlgoNode(self.scene, val)
        if self.len() > 0:
            node.set_next_to(self.nodes[-1], RIGHT, metadata=meta)
        else:
            node.grp.move_to(self.displacement)
        self.nodes.append(node)
        # Update positioning of list
        node.show(metadata=meta, animated=animated, w_prev=w_prev)

        # Update the VGroup of the list
        self.group(metadata=meta, immediate_effect=True)

        # Center list
        if center:
            self.center(metadata=meta, animated=animated, w_prev=False)

        # Add metadata if meta is created in this fn
        if metadata is None:
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

        meta = Metadata.check_and_create()

        self.nodes[i].hide(meta, animated)
        self.nodes.remove(self.nodes[i])

        # Update the VGroup of the list
        self.group(metadata=meta)

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
            lower_meta = LowerMetadata(TEMP_META_NAME, action_pair)
            meta.add_lower(lower_meta)

        self.scene.add_metadata(meta)

    @staticmethod
    def align_nodes_from_first_node(algolist, metadata):
        for i in range(1, algolist.len()):
            # algolist.nodes[i].grp.next_to(algolist.nodes[i - 1].grp, RIGHT)
            algolist.nodes[i].set_next_to(algolist.nodes[i - 1], RIGHT, metadata)

    @staticmethod
    def align_nodes_from_last_node(algolist, metadata):
        for i in reversed(range(0, algolist.len() - 1)):
            # algolist.nodes[i].grp.next_to(algolist.nodes[i + 1].grp, LEFT)
            algolist.nodes[i].set_next_to(algolist.nodes[i + 1], LEFT, metadata)

    # enforced contiguous slices
    # move = LEFT or RIGHT, denoting which direction the slice should be shifted in
    def slice(self, start, stop, move=LEFT, animated=True, shift=False, shift_vec=UP):
        # Fix indices if needed
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()

        meta = Metadata.check_and_create()

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
        if shift:
            self.scene.shift_scene(shift_vec, meta)

        # Create sliced list in background
        sublist = AlgoList(self.scene,
                           [n.val for n in self.nodes][start:stop], show=False)

        # Align to its original position in the list
        sublist.nodes[0].set_next_to(self.nodes[start], 0, metadata=meta)
        # sublist.nodes[0].grp.align_to(self.nodes[start].grp, LEFT)
        AlgoList.align_nodes_from_first_node(sublist, metadata=meta)

        hidden_sublist = AlgoList(self.scene,
                                  [n.val for n in self.nodes][start:stop], show=False)

        # Position hidden sliced list by taking reference from last element
        # hidden_sublist.nodes[-1].grp.next_to(self.nodes[stop - 1].grp, DOWN + move)
        hidden_sublist.nodes[-1].set_next_to(self.nodes[stop - 1], DOWN + move, metadata=meta)
        AlgoList.align_nodes_from_last_node(hidden_sublist, metadata=meta)

        sublist.set_next_to(hidden_sublist, vector=0, metadata=meta, animated=True)

        # Get rid of hidden_sublist
        self.scene.remove(hidden_sublist)

        # Add metadata to scene
        self.scene.add_metadata(meta)

        return sublist

    ''' Concatenates this list and other_list, then centres them '''
    def concat(self, other_list, metadata=None, animated=True, w_prev=False, center=False):
        meta = Metadata.check_and_create(metadata)
        # Set other list to the right of this list
        other_list.set_next_to(self, RIGHT, metadata=meta, animated=animated, w_prev=w_prev)

        # Add lists together
        self.nodes += other_list.nodes

        # Update the VGroup of the list
        self.group(metadata=meta)

        if center:
            self.center(metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

        return self

    def merge(self, left_list, right_list, metadata=None, animated=True,
              replace=False, shift=False, shift_vec=UP):
        meta = Metadata.check_and_create(metadata)

        # make hidden copies of left_list and right_list at their respective positions
        left_list_copy = AlgoList(self.scene, [n.val for n in left_list.nodes], show=False)
        left_list_copy.set_next_to(left_list, vector=0)

        right_list_copy = AlgoList(self.scene, [n.val for n in right_list.nodes], show=False)
        right_list_copy.set_next_to(right_list, vector=0)

        # reveal the copies silently
        left_list_copy.show(animated=False)
        right_list_copy.show(animated=False)

        # create a hidden dummy list of the final length and place below the left_list
        left_len = left_list.len()
        right_len = right_list.len()

        final_len = left_len + right_len
        hidden_merged_list = AlgoList(self.scene, [0 for _ in range(0, final_len)], show=False)

        hidden_merged_list.nodes[0].set_next_to(left_list_copy.nodes[0], DOWN, metadata=meta)
        AlgoList.align_nodes_from_first_node(hidden_merged_list, metadata=meta)

        # do the pointer thing and place the respective copied nodes at their respective places
        # keep track of the copied nodes to remove them later -- prob can do this via the left and right lists
        # update the values on hidden dummy list silently

        left_index = 0
        right_index = 0
        curr_index = 0

        merged_list_vals = []

        while left_index < left_len and right_index < right_len:

            fst_left = left_list_copy.nodes[left_index]
            fst_right = right_list_copy.nodes[right_index]

            # highlight the nodes to be compared
            fst_left.highlight(metadata=meta, animated=animated)
            fst_right.highlight(metadata=meta, animated=animated, w_prev=True)

            fst_left.dehighlight(metadata=meta, animated=animated)
            fst_right.dehighlight(metadata=meta, animated=animated, w_prev=True)

            node_to_move = fst_left
            if node_to_move.val > fst_right.val:
                node_to_move = fst_right
                right_index += 1
            else:
                left_index += 1

            # highlight node to move
            node_to_move.highlight(metadata=meta, animated=animated)

            # animate moving node_to_move to (hidden_merged_list.nodes[curr_index], vector=0)
            node_to_move.set_next_to(hidden_merged_list.nodes[curr_index], vector=0, animated=animated,
                                     metadata=meta)

            # track the added value
            merged_list_vals.append(node_to_move.val)

            # increment curr_index
            curr_index += 1

        if left_index == left_len:
            # left list was exhausted
            rem_right = VGroup(*[n.grp for n in right_list_copy.nodes[right_index:]])
            rem_hidden = VGroup(*[n.grp for n in hidden_merged_list.nodes[curr_index:]])

            # highlight right slice
            right_list_copy.highlight(*range(right_index, right_len), metadata=meta, animated=animated)

            merged_list_vals += [n.val for n in right_list_copy.nodes[right_index:]]

            # move it accordingly
            self.move_group_to_group(rem_right, rem_hidden, animated=animated, metadata=meta)
        else:
            # right list was exhausted
            rem_left = VGroup(*[n.grp for n in left_list_copy.nodes[left_index:]])
            rem_hidden = VGroup(*[n.grp for n in hidden_merged_list.nodes[curr_index:]])

            # highlight left slice
            left_list_copy.highlight(*range(left_index, left_len), metadata=meta, animated=animated)

            merged_list_vals += [n.val for n in left_list_copy.nodes[left_index:]]

            # move it accordingly
            self.move_group_to_group(rem_left, rem_hidden, animated=animated, metadata=meta)

        merged_list = AlgoList(self.scene, merged_list_vals, show=False)
        merged_list.set_next_to(hidden_merged_list, vector=0, metadata=meta)

        # show the dummy list
        merged_list.show(animated=False, metadata=meta)
        hidden_merged_list.hide(animated=False, metadata=meta)

        # remove the copied left and right lists
        self.scene.remove(left_list_copy)
        self.scene.remove(right_list_copy)
        self.scene.remove(hidden_merged_list)

        # if replace, call replace (with shift set to false) on the left and right lists
        # if shift, shift scene using the vec
        # TODO

        return hidden_merged_list

    ''' Destroys the given list(s) and moves this list to its/their original position.
     Given lists assumed to be in a single line. '''
    def replace(self, *lists, animated=True, shift=False, shift_vec=UP):
        # get the middle point of all the given lists
        # hide all the given lists
        # move this list to the middle pt found
        # if shift, shift the scene using the vec
        pass
