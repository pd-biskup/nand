from scripts.chip import Chip, NAND, DFF


def test():
    n = Chip('test', 'DEMUX4W')
    # n.show_graph()
    n.tick({'in': 0, 'sel': [1, 1]})
    print([o.value for o in n.output])
    print(n.parts_count())


def test4():
    n = Chip('4b', 'ADD4B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1],
            'in2': [0, 1, 0, 1], 'carryIn': 1})
    print([o.value for o in n.output])
    print(n.parts_count())


def test8():
    n = Chip('8b', 'MUX8B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1, 0, 1, 0, 1],
            'in2': [0, 0, 0, 1, 1, 1, 1, 0], 'sel': 1})
    print([o.value for o in n.output])
    print(n.parts_count())


def test16():
    n = Chip('16b', 'MUX16B')
    # n.show_graph()
    n.tick({'in1': [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
            'in2': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1], 'sel': 1})
    print([o.value for o in n.output])
    print(n.parts_count())

test4()
