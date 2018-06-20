from nand.store import *
from nand.chip import *
from nand.parser import *

store.register('NAND', NAND)
store.register('DFF', DFF)

load_chips()

# ch = store.get('AND8B', 'and')
# ch.tick({'in1': [1, 0, 0, 1, 1, 1, 1, 0], 'in2': [0, 0, 1, 1, 1, 1, 0, 0]})
# print(ch)

test = load_test('AND4B')
test.evaluate()
print(test.summary())
