from nand.core.store import store
import nand.util.config as config


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

    def summary(self):
        inputs = []
        for inpt in self.chip.inputs:
            try:
                values = [''.join([str(val) for val in vals]) for vals in self.test[inpt.name]]
            except TypeError:
                values = [str(val) for val in self.test[inpt.name]]
            inputs.append(TestColumn(inpt.name, values))
        test_outputs = []
        real_outputs = []
        for out in self.chip.outputs:
            try:
                test_values = [''.join([str(val) for val in vals]) for vals in self.test[out.name]]
            except TypeError:
                test_values = [str(val) for val in self.test[out.name]]
            test_outputs.append(TestColumn(out.name, test_values))
            try:
                real_values = [''.join([str(val) for val in vals]) for vals in self.output[out.name]]
            except TypeError:
                real_values = [str(val) for val in self.output[out.name]]
            real_outputs.append(TestColumn(out.name, real_values))
        return TestSummary(inputs, test_outputs, real_outputs)
    
    def __str__(self):
        return f'Test {self.name}'


class TestSummary:

    def __init__(self, inputs, test_outputs, real_outputs):
        self.inputs = inputs
        self.test_outputs = test_outputs
        self.real_outputs = real_outputs
        self.width = 3
        for inpt in self.inputs:
            self.width += inpt.width + 1
        for out in self.test_outputs:
            self.width += out.width + 1
        for out in self.real_outputs:
            self.width += out.width + 1

    def __str__(self):
        text = '+' + (self.width - 2) * '-' + '+' + '\n'
        text += '|'
        for inpt in self.inputs:
            text += inpt.get_label() + '|'
        text += '|'
        for out in self.test_outputs:
            text += out.get_label() + '|'
        text += '|'
        for out in self.real_outputs:
            text += out.get_label() + '|'
        text += '\n'
        text += '+' + (self.width - 2) * '-' + '+' + '\n'
        for i in range(self.inputs[0].length):
            text += '|'
            for inpt in self.inputs:
                text += inpt[i] + '|'
            text += '|'
            tests = {}
            for out in self.test_outputs:
                text += out[i] + '|'
                tests[out.label] = out[i].strip()
            text += '|'
            for out in self.real_outputs:
                if config.color and tests[out.label] != out[i].strip():
                    text += config.colors['red'] + out[i] + config.colors['default'] + '|'
                else:
                    text += out[i] + '|'
            text += '\n'
        text += '+' + (self.width - 2) * '-' + '+' + '\n'
        return text


class TestColumn:

    def __init__(self, label, data):
        self.label = label
        self.data = data
        self.width = max(len(label), len(data[0])) + 2
        self.length = len(data)

    def update_width(self, width):
        if width > self.width:
            self.width = width
    
    def get_label(self):
        return self._justify(self.label)
    
    def _justify(self, text):
        if len(text) > self.width:
            return text
        else:
            spaces = (self.width - len(text)) // 2
            if spaces * 2 == self.width - len(text):
                return ' ' * spaces + text + ' ' * spaces
            else:
                return ' ' * spaces + text + ' ' * (spaces + 1)
    
    def __getitem__(self, key):
        return self._justify(self.data[key])
