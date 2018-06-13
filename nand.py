from nand.store import ChipStore
from nand.parser import Parser
import sys

if __name__ == '__main__':
    store = ChipStore()
    parser = Parser(store)
