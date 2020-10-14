from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        xs = AlgoList(self, [25, 43, 5, 18, 30])
        self.mergeSort(xs)

    def mergeSort(self, xs):
        if xs.len() > 1:
            m = xs.len() // 2
            left = xs.slice(0, m)
            right = xs.slice(m, xs.len())
            left = self.mergeSort(left)
            right = self.mergeSort(right)

            xs = AlgoList(self, [])

            while left.len() > 0 and right.len() > 0:
                if left.get_val(0) < right.get_val(0):
                    xs.append(left.get_val(0))
                    left.pop(0)
                else:
                    xs.append(right.get_val(0))
                    right.pop(0)

            for i in [n.val for n in left.nodes]:
                xs.append(i)
            for i in [n.val for n in right.nodes]:
                xs.append(i)
                
        return xs
