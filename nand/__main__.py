from nand.core.store import store
from nand.core.parser import load_chips, load_test
from nand.core.chip import NAND, DFF
import argparse


def main():
    store.register('NAND', NAND)
    store.register('DFF', DFF)
    load_chips()
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t', dest='test', type=str, help='test name')
    args = parser.parse_args()
    test = load_test(args.test)
    test.evaluate()
    print(test.summary(color=True))


if __name__ == '__main__':
    main()
