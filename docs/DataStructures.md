# Data Structures
Out of the box, we support `List` and `Binary Tree` data structures. Please find the supported operations on these data structures below. First, let's look at how you could extend the library for your data structure.

## Extending Data Structures
In order to extend the library to the data structure of your choice, you must first create a class that extends the `AlgoObject` base class. For this example, let's look at how we can extend the library to `LinkedLists`. Firstly, let us extend the `AlgoNode` object so that each node of our `LinkedList` can have an arrow attached to it.

```python
class AlgoLinkedListNode(AlgoNode):
    def __init__(self, scene, val, next_node=None):
        self.arrow = Arrow(ORIGIN, ORIGIN, stroke_width=5, color=WHITE)
        self.next_node = next_node

        super().__init__(scene, val)
```

In order for the arrow to be shown, we would have to override the `show` method as well.
```python
...
@attach_metadata
def show(self, metadata=None, animated=True, w_prev=False):
    if self.next_node is not None:
        anim_action = self.scene.create_play_action(AlgoTransform(FadeIn(self.arrow)),
            w_prev=w_prev)
        static_action = AlgoSceneAction.create_static_action(self.scene.add, [self.arrow])
        animate_arrow_pair = self.scene.add_action_pair(anim_action, static_action,
            animated=animated)

        # Add Metadata for GUI
        animate_arrow_metadata = LowerMetadata.create(animate_arrow_pair)
        metadata.add_lower(animate_arrow_metadata)
    super().show(metadata=metadata, animated=animated, w_prev=True)
...
```
There are a couple of things to note here. Firstly, every operation that you would like to animate on a Data Structure has to have the decorator `attach_metadata` and these 3 flags: `metadata`, `animated` and `w_prev`.
- The `attach_metadata` decorator and `metadata` flag are used in the GUI to identify animations in the timeline.
- The `animated` flag informs the library on whether to run this operation statically or animate it. 
- Finally, the `w_prev` flag informs whether this operation should be animated concurrently with the previous operation.  

Furthermore, every animation should be added through the `add_action_pair(anim_action, static_action, animated=animated)` method. The complexity here is due to the fact that animations in manim cannot be executed instantly (runtime=0). Therefore, to allow users to be able to skip and set the duration of animations seamlessly, every animation has to be added as a pair - 1 dynamic and 1 static.
- Dynamic actions are created through the `create_play_action` method where `manim` Transforms can be passed in as parameters.
- Static actions are created through the `create_static_action` method where one of `self.scene.add` or `self.scene.remove` or even a custom function that simply rearranges the position / sets the color of objects is passed in together with the arguments for it (similar to `transforms` in `Customizations.md`).

Finally, for every animation we add, we must also add a corresponding `LowerMetadata` for the GUI. Note that we need not write out the animation to show the underlying `AlgoNode` since we have extended the base class!

With this extension to `AlgoNode` now in place, we can now implement the `AlgoLinkedList` class. The creation of this class mainly requires us to be able to arrange the nodes spacially (done through the `next_to` method provided by `manim`).
```python
class AlgoLinkedList(AlgoObject):
    def __init__(self, scene, arr):
        super().__init__(scene)

        # Create nodes
        self.nodes = []
        for val in arr:
            curr_node = AlgoLinkedListNode(scene, val)
            if len(self.nodes) != 0:
                self.nodes[-1].next_node = curr_node
            self.nodes.append(curr_node)

        # Arrange the nodes, setting nodes next to each other
        for i in range(1, len(self.nodes)):
            self.nodes[i].grp.next_to(self.nodes[i - 1].grp, 3 * RIGHT)

        # Initial positioning
        self.grp = VGroup(*[n.grp for n in self.nodes])
        self.center(animated=False)

        # Show all nodes in the list
        for node in self.nodes:
            node.show(animated=False)
```
If you were to run the program as it is now, you would notice that the arrows have not been positioned correctly / missing. This is because we had originally created the arrow and set it to start and end at `ORIGIN` however at runtime, the positions of the nodes would have changed! The way to fix this is through an auxiliary function `set_arrow_start_end`, and of course add it as an `action_pair` in `show`.

```python
class AlgoLinkedListNode(AlgoNode):
    ...
    def set_arrow_start_end(self):
        if self.next_node is None:
            # hide arrow
            self.arrow.set_opacity(0)
        else:
            # set arrow to start at this node and end at next
            start = self.grp.get_right()
            end = self.next_node.grp.get_left()
            self.arrow.put_start_and_end_on(start, end)

    @attach_metadata
    def show(self, metadata=None, animated=True, w_prev=False):
        if self.next_node is not None:
            action = AlgoSceneAction.create_static_action(self.set_arrow_start_end)
            set_arrow_pair = self.scene.add_action_pair(action, action, animated=False)

            ...
            # Add Metadata for GUI
            set_arrow_metadata = LowerMetadata.create(set_arrow_pair)
            metadata.add_lower(set_arrow_metadata)
            ...
```
The other operations on `LinkedList` can be extended in the same way specifying the `action_pairs` and `metadata` to inform the library on how to animate the operation.

## AlgoList
On top of the standard operations supported by Python's list interface, we support further operations that make sorting algorithms work and also some animation functions that can be called in `algo` while the algorithm is executing.  

| Method | Description |
|---------|--------------------------|
| compare(i, j) | compares the values at indices i and j and returns list[i] < list[j]. |
| swap(i, j) | swaps the nodes at indices i and j |
| highlight(i1, i2, ...) | highlights all nodes at indices i1, i2, ... |
| dehighlight(i1, i2, ...) | removes highlight from all nodes at indices i1, i2, ... |
| change_val(i, new_val) | changes and animates the changing of value at index i to new_val |
| get_val(i) | gets value at index i |
| show_list() | shows list from screen |
| hide_list() | hides list from screen |
| append(val) | appends value to list |
| pop() | pops val from list |
| slice(start, stop) | performs list[start:stop] returns the slice|
| concat(other_list) | concatenates this list with another list returns concatenated list|
| merge(left_list, right_list) | merges left_list and right_list and returns merged list |
| empty() | returns whether list is empty |
| len() | returns length of list |

**Note:** Refer to each function's in-line code documentation to check for extra parameters that
 could be useful for your specific use case. 
 Some functions with extra hidden parameters include `merge`, `slice` and `compare`.
  
## AlgoBinaryTree
| Method | Description |
|---------|--------------------------|
| insert(val) | insert val into tree |
| size() | get size of tree |
| find(val) | finds val in tree |

## AlgoBinaryTreeNode
AlgoBinaryTree holds the root of this node, which has `left` and `right` as properties which can be accessed by the user to do a tree traversal (please check out `algomanim_examples/binarytreesort.py`).