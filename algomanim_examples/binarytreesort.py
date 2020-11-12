from manimlib.imports import *
from algomanim.algoscene import AlgoScene, AlgoTransform
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
        algolist = AlgoList(self, unsorted_list, displacement=UP)
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

    # pylint: disable=R0914
    def customize(self, action_pairs):
        pin = self.find_pin("list_elems")[0]
        idx = pin.get_index()

        title_text = TextMobject("First, we insert the elements of the list into a binary tree")
        title_text.to_edge(UP)
        transform = lambda: Write(title_text)
        self.add_transform(idx, transform)

        self.add_wait(idx + 1, wait_time = 0.25)

        self.chain_pin_highlight("inserted_node")

        tree_finished_pin = self.find_pin("finished_tree_build")[0]
        idx2 = tree_finished_pin.get_index()
        self.fast_forward(idx + 2, idx2)
        new_text = TextMobject("Now, we do an INORDER traversal of the tree")
        new_text.to_edge(UP)
        transform = lambda: [FadeOut(title_text), ReplacementTransform(title_text, new_text)]
        self.add_transform(idx2, transform)

        self.chain_pin_highlight("visited_node")

        self.fast_forward(idx2 + 1)
        end_text = TextMobject("We have a sorted list!")
        end_text.to_edge(UP)
        transform = lambda: [FadeOut(new_text), ReplacementTransform(new_text, end_text)]
        self.add_transform(None, transform)

    def chain_pin_highlight(self, pin_str):
        pins = self.find_pin(pin_str)
        prev_node = None
        for pin in pins:
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
