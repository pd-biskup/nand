import argparse
from nand.core.parser import load_test
import nand.util.config as config


class CLI:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--test', '-t', dest='test', type=str,
                                 help='executes test TEST')
        self.parser.add_argument('--data-dir', '-d', dest='data_dir', type=str,
                                 help='path to data directory')
        self.parser.add_argument('--verbose', '-v', dest='verbose', action='count',
                                 help='increases verbosity, can be specified 3 times')
        self.parser.add_argument('--color', '-c', dest='color', type=bool,
                                 help='enables colored output')
        self.args = self.parser.parse_args()
    
    def setup(self):
        if self.args.verbose:
            config.log_level = self.args.verbose
        if self.args.data_dir:
            config.workspace = self.args.data_dir
        if self.args.color:
            config.color = self.args.color

    def run(self):
        if self.args.test:
            test = load_test(self.args.test)
            test.evaluate()
            print(test.summary())
