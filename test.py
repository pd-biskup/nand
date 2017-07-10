from scripts.chip_parser import Parser
from scripts.chip import Chip, NAND, DFF


def test():
    n = Chip('hadd', 'FADD')
    # n.show_graph()
    n.tick({'in1': 1, 'in2': 1, 'carryIn': 0})
    print(str(n.output[0].value) + ' ' + str(n.output[1].value))

test()
