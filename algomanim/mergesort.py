from algomanim.algoscene import AlgoScene
from algomanim.algolist import AlgoList

class MergeSortScene(AlgoScene):
    def algoconstruct(self):
        xs = AlgoList(self, [25, 43, 15, 30])
        self.mergeSort(xs)

    def mergeSort(self, xs):
        self.add_action(self.clear)
        xs.show()
        if xs.len() > 1:
            m = xs.len() // 2
            left = xs.slice(0, m)
            left = self.mergeSort(left)
            right = xs.slice(m, xs.len())
            right = self.mergeSort(right)

            xs.hide()
            xs = AlgoList(self, [])

            while left.len() > 0 and right.len() > 0:
                left.highlight(0)
                right.highlight(0)
                if left.get_val(0) < right.get_val(0):
                    xs.append(left.get_val(0))
                    left.pop(0)
                else:
                    xs.append(right.get_val(0))
                    right.pop(0)

            xs.concat(left)
            xs.concat(right)
                
        return xs
