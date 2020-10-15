from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        algolist = AlgoList(self, [25, 15, 34, 26])
        self.merge_sort(algolist)

    def merge_sort(self, algolist):
        self.add_action(self.clear)
        algolist.center(animated=True)
        algolist.show(animated=False)
        if algolist.len() > 1:
            mid_pt = algolist.len() // 2
            left = algolist.slice(0, mid_pt, animated=True)
            left = self.merge_sort(left)

            self.add_action(self.clear)
            algolist.show(animated=False)
            right = algolist.slice(mid_pt, algolist.len(), animated=True)
            right = self.merge_sort(right)

            self.add_action(self.clear)
            self.add_action(left.grp.shift, *[LEFT*left.len(), DOWN*2])
            self.add_action(right.grp.shift, *[RIGHT*right.len(), DOWN*2])
            left.show(animated=False)
            right.show(animated=False)
            self.add_action(self.wait, 2)
            algolist = AlgoList(self, [])

            while left.len() > 0 and right.len() > 0:
                left.highlight(0)
                right.highlight(0)
                left.dehighlight(0)
                right.dehighlight(0)
                if left.get_val(0) < right.get_val(0):
                    algolist.append(left.get_val(0))
                    left.pop(0)
                else:
                    algolist.append(right.get_val(0))
                    right.pop(0)

            algolist.concat(left)
            algolist.concat(right)
            algolist.center()

        sorted_text = TextMobject("Sorted")
        sorted_text.shift(UP)
        self.add_action(self.play, *[Write(sorted_text)])
        return algolist
