# Data Structures
Out of the box, we support `List` and `Binary Tree` data structures. Please find the supported operations on these data structures below.

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
| remove(val) (TODO) | finds and removes val in tree |
| find(val) | finds val in tree |

## AlgoBinaryTreeNode
AlgoBinaryTree holds the root of this node, which has `left` and `right` as properties which can be accessed by the user to do a tree traversal (please check out `algomanim_examples/binarytreesort.py`).