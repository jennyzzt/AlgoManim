import numpy as np
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata

class AlgoBinaryTreeNode(AlgoNode):
    def __init__(self, scene, val, parent=None):
        self.line = Line(ORIGIN, ORIGIN, stroke_width=5, color=WHITE)
        self.parent = parent
        self.left = None
        self.right = None
        self.id = None # pylint: disable=C0103

        self.recursive_update_depth()

        super().__init__(scene, val)

    def set_left(self, left):
        self.left = left
        self.left.parent = self
        self.recursive_update_depth()

    def set_right(self, right):
        self.right = right
        self.right.parent = self
        self.recursive_update_depth()

    def recursive_size(self):
        num_nodes = 1
        if self.left:
            num_nodes += self.left.recursive_size()
        if self.right:
            num_nodes += self.right.recursive_size()
        return num_nodes

    def recursive_insert(self, val):
        curr_node = self
        # If value is less than curr_node, insert to the left
        if val < curr_node.val:
            if curr_node.left is None:
                new_node = AlgoBinaryTreeNode(curr_node.scene, val, curr_node)
                curr_node.set_left(new_node)
                return new_node
            curr_node = curr_node.left
        # Else insert to the right
        else:
            if curr_node.right is None:
                new_node = AlgoBinaryTreeNode(curr_node.scene, val, curr_node)
                curr_node.set_right(new_node)
                return new_node
            curr_node = curr_node.right
        # curr_node is filled, try next one
        return curr_node.recursive_insert(val)

    def recursive_update_depth(self):
        if self.parent is None:
            self.id = 1
            self.depth = 1
        else:
            self.depth = self.parent.depth + 1
            if self.parent.left == self:
                self.id = self.parent.id * 2
            else:
                self.id = self.parent.id * 2 + 1

        if self.left is not None:
            self.left.recursive_update_depth()

        if self.right is not None:
            self.right.recursive_update_depth()

    def recursive_show(self, max_depth, metadata=None, animated=True, w_prev=False):
        self.show(max_depth, metadata=metadata, animated=animated, w_prev=w_prev)
        if self.left is not None:
            self.left.recursive_show(max_depth, metadata=metadata, animated=animated,
                w_prev=w_prev)

        if self.right is not None:
            self.right.recursive_show(max_depth, metadata=metadata, animated=animated,
                w_prev=w_prev)

    def set_line_start_end(self, parent):
        if parent is None:
            # reset line
            self.line.set_opacity(0)
        else:
            center = self.grp.get_center()
            parent_center = parent.grp.get_center()
            pos_y = center[1] - parent_center[1]
            pos_x = center[0] - parent_center[0]
            angle = np.arctan2(pos_y, pos_x)
            start = center - \
                self.scene.settings['node_size'] / 2 * np.array([np.cos(angle), np.sin(angle), 0])
            end = parent_center + \
                self.scene.settings['node_size'] / 2 * np.array([np.cos(angle), np.sin(angle), 0])
            self.line.put_start_and_end_on(start, end)

    def get_x_pos(self, node_id, max_depth):
        # finding the id of the middle leaf node OF THE WHOLE TREE
        total_leaf_nodes = 2 ** (max_depth - 1)
        middle_node_id = 2 ** (max_depth - 1) + (total_leaf_nodes - 1) / 2

        return int(middle_node_id - node_id) * \
            ((self.scene.settings['node_size'] + 0.5) * LEFT)

    def show(self, max_depth, metadata=None, animated=True, w_prev=False): # pylint: disable=W0221:
        levels = max_depth - self.depth

        # the 2 leaf nodes that this node needs to be at the center of
        leftmost_id = self.id * (2 ** levels)
        rightmost_id = leftmost_id + (2 ** levels) - 1

        pos_x = (self.get_x_pos(leftmost_id, max_depth) +
                    self.get_x_pos(rightmost_id, max_depth)) / 2
        pos_y = (self.depth - 1) * ((self.scene.settings['node_size'] + 0.5) * DOWN)

        self.grp.move_to(pos_x + pos_y)
        if self.parent is not None:
            action = AlgoSceneAction.create_static_action(self.set_line_start_end, [self.parent])
            self.scene.add_action_pair(action, action, animated=False)

            anim_action = self.scene.create_play_action(AlgoTransform(FadeIn(self.line)),
                w_prev=w_prev)
            static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.line])
            self.scene.add_action_pair(anim_action, static_action, animated=animated)

        super().show(metadata, animated, True)


class AlgoBinaryTree:
    def __init__(self, scene, max_depth, root=None, show=True):
        self.root = root
        self.max_depth = max_depth + 1
        self.scene = scene

        if show:
            self.show_tree(animated=False)

    def show_tree(self, metadata=None, animated=True, w_prev=False):
        ''' Display Tree on Sceen '''
        if self.root is not None:
            meta = Metadata.check_and_create(metadata)

            self.root.recursive_show(self.max_depth, metadata=meta, animated=animated,
                w_prev=w_prev)

            # Add metadata if meta is created in this fn
            if metadata is None:
                self.scene.add_metadata(meta)

    def insert(self, val, metadata=None, animated=True, w_prev=False):
        ''' Insert element into tree '''
        meta = Metadata.check_and_create(metadata)

        new_node = self.root.recursive_insert(val)
        new_node.recursive_show(self.max_depth, metadata=meta, animated=animated,
            w_prev=w_prev)

        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    def size(self):
        ''' Returns the total number of nodes of the tree '''
        return self.root.recursive_size()