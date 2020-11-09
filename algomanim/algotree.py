# pylint: disable=C0103, R0904, W0105
from enum import Enum, auto
from manimlib.imports import *
from algomanim.algonode import AlgoNode
from algomanim.algoscene import AlgoTransform, AlgoSceneAction
from algomanim.metadata import Metadata, LowerMetadata
from algomanim.settings import Shape

class TreeTraversalType(Enum):
    PREORDER = auto()
    INORDER = auto()
    POSTORDER = auto()

class AlgoTreeNode(AlgoNode):
    def __init__(self, scene, val, parent=None):
        # default node configs for treenodes
        scene.settings['node_shape'] = Shape.CIRCLE

        super().__init__(scene, val)
        self.left = None
        self.right = None
        self.parent = parent

        self.nodesgrp = None
        self.linesgrp = None
        self.treegrp = None

        # features used for positioning
        self.x = -1
        self.y = -1

        # for visualisation
        self.line = Line(ORIGIN, ORIGIN, stroke_width=10, color=WHITE)

    def static_set_line_with(self, parent):
        if parent is None:
            # reset line
            self.line.put_start_and_end_on(self.grp.get_center(),
                                           self.grp.get_center()+[0.1, 0, 0])
        else:
            self.line.put_start_and_end_on(self.grp.get_center(), parent.grp.get_center())

    # Set the line connecting the node to its parent
    def set_line_with(self, parent=None):
        action = AlgoSceneAction.create_static_action(self.static_set_line_with, [parent])
        self.scene.add_action_pair(action, action, animated=False)

    # ----- Visualization Positioning Helper Functions ----- #

    # Calculate the relative x, y coords of the nodes
    # (knuth algorithm)
    def calc_layout(self, depth=0, i=0):
        # Assign x and y coords to left children nodes
        if self.left:
            i = self.left.calc_layout(depth+1, i)
        # Assign x and y coords to this node
        self.x = i
        self.y = depth
        i += 1
        # Assign x and y coords to right children nodes
        if self.right:
            i = self.right.calc_layout(depth+1, i)
        return i

    # Fit the node's position to its x, y fields relative to the root
    def fit_layout(self, parent=None):
        # If node now has no parent, reset connecting line
        if parent is None:
            self.set_line_with()
        # Else set node with relative to parent
        else:
            x_diff = self.x - parent.x
            y_diff = self.y - parent.y
            relative_vector = (RIGHT*x_diff+DOWN*y_diff)*self.node_length
            # set node position
            self.set_relative_of(parent, relative_vector)
            # set node's line position
            self.set_line_with(parent)
        if self.left:
            self.left.fit_layout(self)
        if self.right:
            self.right.fit_layout(self)

    # Recalculate and fit nodes to layout
    def adjust_layout(self):
        root = self
        while root.parent:
            root = root.parent
        root.calc_layout()
        root.fit_layout()
        root.treegroup()
    # ---------------------------------------------------- #

    # Get a list of all tree nodes with this node as the root
    def get_all_nodes(self):
        nodes = []
        nodes.append(self)
        if self.left:
            nodes += self.left.get_all_nodes()
        if self.right:
            nodes += self.right.get_all_nodes()
        return nodes

    # Treegroup all tree nodes and lines together
    def treegroup(self):
        nodes = self.get_all_nodes()
        self.nodesgrp = VGroup(*[n.grp for n in nodes])
        self.linesgrp = VGroup(*[n.line for n in nodes])
        self.treegrp = VGroup(*[self.nodesgrp, self.linesgrp])

    ''' Center the tree on screen '''
    def center_tree(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Create action pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.treegrp.center], transform=ApplyMethod), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.treegrp.center)
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Create LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, [self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # ------------- Show Helper Functions ------------- #

    # Show only the line connecting this node to the parent
    def show_line(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Add show line action_pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.line], transform=FadeIn), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.line])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Send line to back
        pos_action = AlgoSceneAction.create_static_action(self.scene.bring_to_back, [self.line])
        self.scene.add_action_pair(pos_action, pos_action, animated=animated)
        # Initialise a LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, val=[self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Show both the node and the line connecting it
    def show(self, metadata=None, animated=True, w_prev=False):
        self.show_line(metadata=metadata, animated=animated, w_prev=w_prev)
        super().show(metadata=metadata, animated=animated, w_prev=w_prev)

    # Recursely show entire tree with this node as the root
    def recurse_show_tree(self, order, metadata=None, animated=True, w_prev=False):
        if order == TreeTraversalType.PREORDER:
            self.show(metadata=metadata, animated=animated, w_prev=w_prev)
        if self.left:
            self.left.recurse_show_tree(order, metadata=metadata, animated=animated, w_prev=w_prev)
        if order == TreeTraversalType.INORDER:
            self.show(metadata=metadata, animated=animated, w_prev=w_prev)
        if self.right:
            self.right.recurse_show_tree(order, metadata=metadata, animated=animated, w_prev=w_prev)
        if order == TreeTraversalType.POSTORDER:
            self.show(metadata=metadata, animated=animated, w_prev=w_prev)

    ''' Adjust tree structure and show '''
    def show_tree(self, order=TreeTraversalType.PREORDER,
                  metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        self.adjust_layout()
        self.recurse_show_tree(order, meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)
    # ---------------------------------------------------- #

    # ------------- Hide Helper Functions ------------- #

    # Hide only the line connecting this node to the parent
    def hide_line(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # Add hide line action_pair
        anim_action = self.scene.create_play_action(
            AlgoTransform([self.line], transform=FadeOut), w_prev=w_prev
        )
        static_action = AlgoSceneAction.create_static_action(self.scene.remove, [self.line])
        action_pair = self.scene.add_action_pair(anim_action, static_action, animated=animated)
        # Initialise LowerMetadata
        lower_meta = LowerMetadata.create(action_pair, val=[self.val])
        meta.add_lower(lower_meta)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    # Hide both the node and the line connecting it
    def hide(self, metadata=None, animated=True, w_prev=False):
        self.hide_line(metadata, animated=animated, w_prev=w_prev)
        super().hide(metadata, animated=animated, w_prev=w_prev)

    # Recursely hide entire tree with this node as the root
    def recurse_hide_tree(self, order, metadata=None, animated=True, w_prev=False):
        if order == TreeTraversalType.PREORDER:
            self.hide(metadata=metadata, animated=animated, w_prev=w_prev)
        if self.left:
            self.left.recurse_hide_tree(order, metadata=metadata, animated=animated, w_prev=w_prev)
        if order == TreeTraversalType.INORDER:
            self.hide(metadata=metadata, animated=animated, w_prev=w_prev)
        if self.right:
            self.right.recurse_hide_tree(order, metadata=metadata, animated=animated, w_prev=w_prev)
        if order == TreeTraversalType.POSTORDER:
            self.hide(metadata=metadata, animated=animated, w_prev=w_prev)

    ''' Hide entire tree with this node as root '''
    def hide_tree(self, order=TreeTraversalType.PREORDER,
                  metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        self.adjust_layout()
        self.recurse_hide_tree(order, meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)
    # ---------------------------------------------------- #

    ''' Returns the total number of nodes of the tree '''
    def size(self):
        num_nodes = 1
        if self.left:
            num_nodes += self.left.size()
        if self.right:
            num_nodes += self.right.size()
        return num_nodes

    def insert(self, val, animated=True):
        curr_node = self
        # If value is less than curr_node, insert to the left
        if val < curr_node.val:
            if curr_node.left is None:
                curr_node.left = AlgoTreeNode(curr_node.scene, val, curr_node)
                return
            curr_node = curr_node.left
        # Else insert to the right
        else:
            if curr_node.right is None:
                curr_node.right = AlgoTreeNode(curr_node.scene, val, curr_node)
                return
            curr_node = curr_node.right
        # curr_node is filled, try next one
        curr_node.insert(val, animated)

    # Returns the minimum value node in the tree
    # which is the left most node in this case
    def min_val_node(self):
        curr_node = self
        while curr_node.left:
            curr_node = curr_node.left
        return curr_node

    # Returns true if node has parent
    def is_child(self):
        return self.parent is not None

    # Returns true if node is left of parent
    def is_left(self):
        return self.parent.left == self

    ''' Swap this tree node with another tree node '''
    def swap(self, node, metadata=None, animated=True, w_prev=False):
        # this fn should only be used with other tree nodes
        if not isinstance(node, AlgoTreeNode):
            raise ValueError('Inappropriate type: {} for node whereas a  \
            AlgoTreeNode is expected'.format(type(node)))
        meta = Metadata.check_and_create(metadata)
        # update parents' children
        if self.is_child():
            if self.is_left():
                self.parent.left = node
            else:
                self.parent.right = node
        if node.is_child():
            if node.is_left():
                node.parent.left = self
            else:
                node.parent.right = self
        # update parents
        ptemp = self.parent
        self.parent = node.parent
        node.parent = ptemp
        # update children
        ltemp = self.left
        rtemp = self.right
        self.left = node.left
        self.right = node.right
        node.left = ltemp
        node.right = rtemp
        # add swap animation
        self.swap_with(node, metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Delete a tree node '''
    def delete(self, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        # remove parent's connection to it
        if self.is_child():
            if self.is_left():
                self.parent.left = None
            else:
                self.parent.right = None
        self.parent = None
        # remove children's connection to it
        if self.left:
            self.left.parent = None
        if self.right:
            self.right.parent = None
        self.left = None
        self.right = None
        # add animation hide node
        self.hide(metadata=meta, animated=animated, w_prev=w_prev)
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)

    ''' Find a value in the tree '''
    def find(self, val):
        node_found = None
        # Recursively finds the node with val
        if val < self.val:
            # If value is lesser, look in left subtree
            node_found = self.left.find(val)
        elif val > self.val:
            # If value is greater, look in right subtree
            node_found = self.right.find(val)
        else:
            # Found node with val
            node_found = self
        # Return node with value if found else it is None
        return node_found

    ''' Finds and remove a value from the tree '''
    def remove(self, val, metadata=None, animated=True, w_prev=False):
        meta = Metadata.check_and_create(metadata)
        new_root = self
        if val < self.val:
            # If value is lesser, look in left subtree
            if self.left is None:
                # No value found to be deleted
                return self
            self.left = self.left.remove(val, metadata=meta, animated=animated, w_prev=w_prev)
        elif val > self.val:
            # If value is bigger, look in right subtree
            if self.right is None:
                # No value found to be deleted
                return self
            self.right = self.right.remove(val, metadata=meta, animated=animated, w_prev=w_prev)
        else:
            # found node with val to be deleted
            if self.left is None:
                self.delete(metadata=meta, animated=animated, w_prev=w_prev)
                new_root = self.right
            elif self.right is None:
                self.delete(metadata=meta, animated=animated, w_prev=w_prev)
                new_root = self.left
            else:
                # node with two children, get the inorder successor
                succ = self.right.min_val_node()
                self.swap(succ, metadata=meta, animated=animated, w_prev=False)
                self.delete(metadata=meta, animated=animated, w_prev=False)
                new_root = succ
        # Add metadata if meta is created in this fn
        if metadata is None:
            self.scene.add_metadata(meta)
        # Adjust layout
        if new_root:
            new_root.adjust_layout()
        return new_root
