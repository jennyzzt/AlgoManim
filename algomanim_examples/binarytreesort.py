from manimlib.imports import *
from algomanim.algoscene import AlgoScene, AlgoSceneAction, AlgoTransform
from algomanim.algolist import AlgoList
from algomanim.algobinarytree import AlgoBinaryTree, AlgoBinaryTreeNode
from algomanim.shape import Shape

class BinaryTreeSortScene(AlgoScene):
    def preconfig(self, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = Shape.CIRCLE
        settings['highlight_color'] = RED

    def inorder_traversal(self, node, curr_list):
        if node is None:
            return
        self.inorder_traversal(node.left, curr_list)
        self.insert_pin("visited_node", node)
        curr_list.append(node.val)
        self.inorder_traversal(node.right, curr_list)

    def algoconstruct(self):
        unsorted_list = [25, 43, 5, 18, 30, 3, 50]
        algolist = AlgoList(self, unsorted_list)
        self.insert_pin("list_elems", *algolist.nodes)

        self.insert_pin("inserted_node", algolist.nodes[0])
        root = AlgoBinaryTreeNode(self, algolist.nodes[0].val)
        algotree = AlgoBinaryTree(self, 3, root)
        for node in algolist.nodes[1:]:
            self.insert_pin("inserted_node", node)
            algotree.insert(node.val)

        sorted_list = AlgoList(self, [], displacement=3.5 * DOWN + 2.125 * LEFT)
        self.inorder_traversal(root, sorted_list)

    def customize(self, action_pairs):
        pin = self.find_pin("list_elems")[0]
        nodes = pin.get_args()
        idx = pin.get_index()
        action = AlgoSceneAction.create_static_action(
            lambda *nodes: [node.grp.move_to(node.grp.get_center() + UP) for node in nodes],
            args=nodes)
        self.add_action_pair(action, index=idx)
        self.add_wait(idx + 1, wait_time = 0.5)

        visited_pins = self.find_pin("inserted_node")
        prev_node = None
        for pin in visited_pins:
            node = pin.get_args()[0]
            anim_action = self.create_play_action(
                AlgoTransform([node.node.set_fill,
                    self.settings['highlight_color']], transform=ApplyMethod,
                    color_index=1), w_prev=False
            )
            self.add_action_pair(anim_action, index=pin.get_index())
            if prev_node is not None:
                anim_action = self.create_play_action(
                    AlgoTransform([prev_node.node.set_fill,
                        self.settings['node_color']], transform=ApplyMethod,
                        color_index=1), w_prev=True
                )
                self.add_action_pair(anim_action, index=pin.get_index()+1)
            prev_node = node

        visited_pins = self.find_pin("visited_node")
        prev_node = None
        for pin in visited_pins:
            node = pin.get_args()[0]
            anim_action = self.create_play_action(
                AlgoTransform([node.node.set_fill,
                    self.settings['highlight_color']], transform=ApplyMethod,
                    color_index=1), w_prev=False
            )
            self.add_action_pair(anim_action, index=pin.get_index())
            if prev_node is not None:
                anim_action = self.create_play_action(
                    AlgoTransform([prev_node.node.set_fill,
                        self.settings['node_color']], transform=ApplyMethod,
                        color_index=1), w_prev=True
                )
                self.add_action_pair(anim_action, index=pin.get_index()+1)
            prev_node = node
