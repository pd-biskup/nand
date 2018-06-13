from nand.store import *
from nand.chip import *
from nand.parser import *

store.register('NAND', NAND)
store.register('DFF', DFF)

load_chips()

no = store.get('NOT', 'not')
no.tick({'in': 0})
print(no.outputs[0].value)
