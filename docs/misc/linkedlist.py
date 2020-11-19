from manimlib.imports import *
from algomanim.algoscene import AlgoScene
from algomanim.algolinkedlist import AlgoLinkedList

class LinkedListScene(AlgoScene):
    def algo(self):
        my_list = [15, 4, 12, 13, 1]
        algoll = AlgoLinkedList(self, my_list)