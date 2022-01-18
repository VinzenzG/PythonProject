import numpy
import numpy as np


def test_order_from_middle():
    actions1 = [0,1,2,3,4,5,6]
    actions2 = [0]
    actions3 = [0,2,4,5]
    actions4 = [1,2,3]
    from agents.agent_minimax.newOrder import order_from_middle
    firstorder = order_from_middle(actions1)
    firstorder1 = order_from_middle(actions2)
    firstorder2 = order_from_middle(actions3)
    firstorder3 = order_from_middle(actions4)

    assert firstorder == [3, 4, 2, 5, 1, 6, 0]
    assert firstorder1 == [0]
    assert firstorder2 == [4, 2, 5, 0]
    assert firstorder3 == [2, 3, 1]

