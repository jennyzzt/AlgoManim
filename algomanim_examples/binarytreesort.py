from manimlib.imports import *
from algomanim.algoscene import AlgoScene, AlgoSceneAction, AlgoTransform
from algomanim.algolist import AlgoList
from algomanim.algobinarytree import AlgoBinaryTree, AlgoBinaryTreeNode
from algomanim.shape import Shape

class BinaryTreeSortScene(AlgoScene):
    def preconfig(self, settings):
        settings['node_size'] = 0.5
        settings['node_shape'] = Shape.CIRCLE
        settings['highlight_color'] = "#e74c3c" # red

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

        self.insert_pin("finished_tree_build")
        sorted_list = AlgoList(self, [], displacement=3.5 * DOWN)
        self.inorder_traversal(root, sorted_list)

    def customize(self, action_pairs):
        pin = self.find_pin("list_elems")[0]
        nodes = pin.get_args()
        idx = pin.get_index()
        action = AlgoSceneAction.create_static_action(
            lambda *nodes: [node.grp.move_to(node.grp.get_center() + UP) for node in nodes],
            args=nodes)
        self.add_action_pair(action, index=idx)
        title_text = TextMobject("First, we insert the elements of the list into a binary tree")
        title_text.to_edge(UP)
        transform = lambda: Write(title_text)
        self.add_transform(idx + 1, transform)

        self.add_wait(idx + 2, wait_time = 0.25)
        
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

        tree_finished_pin = self.find_pin("finished_tree_build")[0]
        idx2 = tree_finished_pin.get_index()
        self.fast_forward(idx + 3, idx2)
        new_text = TextMobject("Now, we do an INORDER traversal of the tree")
        new_text.to_edge(UP)
        transform = lambda: [FadeOut(title_text), ReplacementTransform(title_text, new_text)]
        self.add_transform(idx2, transform)

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

        self.fast_forward(idx2 + 1)
        end_text = TextMobject("We have a sorted list!")
        end_text.to_edge(UP)
        transform = lambda: [FadeOut(new_text), ReplacementTransform(new_text, end_text)]
        self.add_transform(None, transform)
