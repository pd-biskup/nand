from nand.store import store


class Test:

    def __init__(self, name, description, chip, test):
        self.name = name
        self.description = description
        self.chip = store.get(chip, 'test')
        self.test = test
        self.evaluated = False
        self.output = None

    def evaluate(self):
        if not self.evaluated:
            self.output = {}
            for out in self.chip.outputs:
                self.output[out.name] = []
            for step in range(len(list(self.test.values())[0])):
                inpts = {}
                for inpt in self.chip.inputs:
                    inpts[inpt.name] = self.test[inpt.name][step]
                self.chip.tick(inpts)
                for out in self.chip.outputs:
                    self.output[out.name].append(out.value)
            self.evaluated = True

    def summary(self, color=True):
        text = f'{self.name}\n'
        if self.evaluated:
            text = f'{self.name}\n'
            test_length = 0
            for name, value in self.output.items():
                test_length += max(len(name), len(str(value[0]))) + 2
            text += ' ' * (test_length - 8) + 'expected' + ' ' * (test_length - 6) + 'result\n'
            for name, value in self.output.items():
                length = max(len(name), len(str(value[0]))) + 2
                text += f'{name:>{length}}' * 2
            text += '\n'
            for i in range(len(list(self.test.values())[0])):
                for name in self.output:
                    length = max(len(name), len(str(self.test[name][i]))) + 2
                    text += f'{str(self.test[name][i]):>{length}}'
                for name, value in self.output.items():
                    length = max(len(name), len(str(value[i]))) + 2
                    text += f'{str(value[i]):>{length}}'
                text += '\n'
        else:
            text += 'Not evaluated'
        return text
    
    def __str__(self):
        return f'Test {self.name}'
