from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList
from manimlib.imports import *

class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        xs = AlgoList(self, [25, 15, 34, 26])
        self.mergeSort(xs)

    def mergeSort(self, xs):
        self.add_action(self.clear)
        xs.center(animated=True)
        xs.show(animated=False)
        if xs.len() > 1:
            m = xs.len() // 2
            left = xs.slice(0, m, animated=True)
            left = self.mergeSort(left)

            self.add_action(self.clear)
            xs.show(animated=False)
            right = xs.slice(m, xs.len(), animated=True)
            right = self.mergeSort(right)
            
            self.add_action(self.clear)
            self.add_action(left.grp.shift, *[LEFT*left.len(), DOWN*2])
            self.add_action(right.grp.shift, *[RIGHT*right.len(), DOWN*2])
            left.show(animated=False)
            right.show(animated=False)
            self.add_action(self.wait, 2)
            xs = AlgoList(self, [])
            
            while left.len() > 0 and right.len() > 0:
                left.highlight(0)
                right.highlight(0)
                left.dehighlight(0)
                right.dehighlight(0)
                if left.get_val(0) < right.get_val(0):
                    xs.append(left.get_val(0))
                    left.pop(0)
                else:
                    xs.append(right.get_val(0))
                    right.pop(0)
                    
            xs.concat(left)
            xs.concat(right)
        
        sortedText = TextMobject("Sorted")
        sortedText.shift(UP)
        self.add_action(self.play, *[Write(sortedText)])
        return xs
