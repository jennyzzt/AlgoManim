from manimlib.imports import *
from algomanim.algoscene import AlgoTransform

# pylint: disable=R0914
def my_customize(scene, action_pairs):
    pin = scene.find_pin("list_elems")[0]
    idx = pin.get_index()

    title_text = TextMobject("First, we insert the elements of the list into a binary tree")
    title_text.to_edge(UP)
    transform = lambda: Write(title_text)
    scene.add_transform(idx, transform)

    scene.add_wait(idx + 1, wait_time = 0.25)

    chain_pin_highlight(scene, "inserted_node")

    tree_finished_pin = scene.find_pin("finished_tree_build")[0]
    idx2 = tree_finished_pin.get_index()
    scene.fast_forward(idx + 2, idx2)
    new_text = TextMobject("Now, we do an INORDER traversal of the tree")
    new_text.to_edge(UP)
    transform = lambda: [FadeOut(title_text), ReplacementTransform(title_text, new_text)]
    scene.add_transform(idx2, transform)

    chain_pin_highlight(scene, "visited_node")

    scene.fast_forward(idx2 + 1)
    end_text = TextMobject("We have a sorted list!")
    end_text.to_edge(UP)
    transform = lambda: [FadeOut(new_text), ReplacementTransform(new_text, end_text)]
    scene.add_transform(None, transform)

def chain_pin_highlight(scene, pin_str):
    pins = scene.find_pin(pin_str)
    prev_node = None
    for pin in pins:
        node = pin.get_args()[0]
        anim_action = scene.create_play_action(
            AlgoTransform([node.node.set_fill,
                scene.settings['highlight_color']], transform=ApplyMethod,
                color_index=1), w_prev=False
        )
        scene.add_action_pair(anim_action, index=pin.get_index())
        if prev_node is not None:
            anim_action = scene.create_play_action(
                AlgoTransform([prev_node.node.set_fill,
                    scene.settings['node_color']], transform=ApplyMethod,
                    color_index=1), w_prev=True
            )
            scene.add_action_pair(anim_action, index=pin.get_index()+1)
        prev_node = node
