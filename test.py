from scripts.chip_parser import Parser
from scripts.chip import Chip, NAND, DFF


def test():
    n = Chip('reg', 'REG')
    # n.show_graph()
    n.tick({'in': 1, 'load': 1})
    print(n.output[0].value)
    n.tick({'in': 0, 'load': 1})
    print(n.output[0].value)
    n.tick({'in': 1, 'load': 0})
    print(n.output[0].value)
    n.tick({'in': 1, 'load': 1})
    print(n.output[0].value)
    n.tick({'in': 0, 'load': 0})
    print(n.output[0].value)

# test()
