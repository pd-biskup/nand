from nand.core.store import store
from nand.core.parser import load_chips, load_test
from nand.core.chip import NAND, DFF
from nand.util.cli import CLI


def main():
    cli = CLI()
    cli.setup()
    store.register('NAND', NAND)
    store.register('DFF', DFF)
    load_chips()
    cli.run()


if __name__ == '__main__':
    main()
