from scripts.chip import Chip, NAND, DFF


def test():
    n = Chip('or4b', 'OR4B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1], 'in2': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1]})
    print([o.value for o in n.output])


def test4():
    n = Chip('or4b', 'OR4B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1],
            'in2': [0, 1, 0, 1]})
    print([o.value for o in n.output])


def test8():
    n = Chip('or8b', 'OR8B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1, 0, 1, 0, 1],
            'in2': [0, 0, 0, 1, 1, 1, 1, 0]})
    print([o.value for o in n.output])


def test16():
    n = Chip('or16b', 'OR16B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
            'in2': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1]})
    print([o.value for o in n.output])

test16()
