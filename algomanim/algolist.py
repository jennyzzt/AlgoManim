# pylint: disable=E1101, W0105, R0913
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata
from algomanim.algoobject import AlgoObject

class AlgoList(AlgoObject):
    def __init__(self, scene, arr):
        super().__init__(scene)
        # Make and arrange nodes
        self.nodes = [AlgoNode(scene, val) for val in arr]
        for i in range(1, len(self.nodes)):
            self.nodes[i].set_next_to(self.nodes[i-1], RIGHT)
        # Group nodes together
        self.grp = None
        self.group()
        # Initial positioning
        self.center(animated=False)
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
    def group(self):
        self.grp = VGroup(*[n.grp for n in self.nodes])

    ''' Display the list on screen '''
    def show_list(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Show all nodes in the list
        for node in self.nodes:
            node.show(metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Hide the list from screen '''
    def hide_list(self, metadata=None, animated=True, w_prev=False):
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
    def append(self, val, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create new node and add to the right of the list
        node = AlgoNode(self.scene, val)
        if self.len() > 0:
            node.set_next_to(self.nodes[-1], RIGHT, metadata=meta)
        self.nodes.append(node)
        # Update positioning of list
        node.show(metadata=meta, animated=animated, w_prev=w_prev)
        self.group()
        self.center(metadata=meta, animated=animated, w_prev=w_prev)
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

    # removed step parameter for now
    def slice(self, start, stop, animated=True):
        if start < 0:
            start = 0
        if stop > self.len():
            stop = self.len()

        meta = Metadata.check_and_create()

        # Highlight the sublist we want to keep
        self.highlight(*range(start, stop), animated=animated, metadata=meta)

        # Dehighlight the sublist we want to keep
        self.dehighlight(*range(start, stop), animated=animated, metadata=meta)

        # Make a copy of the current list
        # deepcopy doesn't work!
        sublist = AlgoList(self.scene, [n.val for n in self.nodes])

        # Remove the unsliced nodes in reverse order so the indices are still valid after popping
        # This ensures the sliced nodes are in their original positions
        rem_indices = []
        for i, _ in enumerate(sublist.nodes):
            if i not in range(start, stop):
                rem_indices.append(i)
        for i in sorted(rem_indices, reverse=True):
            sublist.pop(i, animated=True)

        # Shift sublist below original list
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

        # Create LowerMetaData
        lower_meta = LowerMetadata('temp', action_pair)
        meta.add_lower(lower_meta)

        # Center the two lists
        grp = VGroup(self.grp, sublist.grp)

        anim_action = self.scene.create_play_action(
            AlgoTransform([grp.center], transform=ApplyMethod)
        )
        static_action = AlgoSceneAction.create_static_action(grp.center)
        action_pair = self.scene.add_action_pair(anim_action, static_action,
                                                 animated=animated)

        # Create LowerMetaData
        lower_meta = LowerMetadata('temp', action_pair)
        meta.add_lower(lower_meta)

        # Add metadata to scene
        self.scene.add_metadata(meta)

        return sublist

    ''' Concatenates this list and other_list, then centres them '''
    def concat(self, other_list, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Add lists together
        self.nodes += other_list.nodes
        # Set other list to the right of this list
        other_list.set_next_to(self, RIGHT, metadata=meta)
        # Update the VGroup of list nodes
        self.group()
        self.center(metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

        return self