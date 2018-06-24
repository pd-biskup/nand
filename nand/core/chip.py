# import networkx as nx
# from matplotlib import pyplot as plt
import re
from nand.core.store import store


class ChipInfo:

    def __init__(self, code, description, inputs, outputs, chips, wires):
        self.code = code
        self.description = description
        self.inputs = inputs
        self.outputs = outputs
        self.chips = chips
        self.wires = wires

    def build(self, name):
        return Chip(name, self.code, self.description, self.inputs, self.outputs, self.chips, self.wires)


class Chip:

    def __init__(self, name, code, description, inputs, outputs, chips, wires):
        self.name = name
        self.code = code
        self.description = description
        self.inputs = []
        for input in inputs:
            if input[-1] == ']':
                bus = re.split(r'\[|\]', input)
                count = int(bus[1])
                self.inputs.append(Bus(bus[0], count, self))
            else:
                self.inputs.append(Pin(input, self))
        self.outputs = []
        for output in outputs:
            if output[-1] == ']':
                bus = re.split(r'\[|\]', output)
                count = int(bus[1])
                self.outputs.append(Bus(bus[0], count, self))
            else:
                self.outputs.append(Pin(output, self))
        self.chips = []
        for ch in chips:
            self.chips.append(store.get(ch['type'], ch['name']))
        self.wires = []
        for wire in wires:
            pin1 = None
            pin2 = None

            if '.' not in wire['in'] and '[' not in wire['in']:
                for input in self.inputs:
                    if input.name == wire['in']:
                        pin1 = input
                        break
            elif '[' not in wire['in']:
                wire_in = wire['in'].split('.')
                for ch in self.chips:
                    if ch.name == wire_in[0]:
                        for output in ch.outputs:
                            if output.name == wire_in[1]:
                                pin1 = output
                                break
                        break
            elif '.' not in wire['in']:
                pin = re.split(r'\[|\]', wire['in'])
                if ':' in pin[1]:
                    sl = pin[1].split(':')
                    for input in self.inputs:
                        if input.name == pin[0]:
                            if sl[0] == '':
                                sl[0] = 1
                            else:
                                sl[0] = int(sl[0])
                            if sl[1] == '':
                                sl[1] = len(input)
                            else:
                                sl[1] = int(sl[1])
                            pin1 = BusSlice(input, sl[0], sl[1])
                            break
                else:
                    for input in self.inputs:
                        if input.name == pin[0]:
                            pin_nr = int(pin[1])
                            pin1 = input[pin_nr - 1]
            else:
                pin = re.split(r'\[|\]|\.', wire['in'])
                if ':' in pin[2]:
                    sl = pin[2].split(':')
                    for ch in self.chips:
                        if ch.name == wire['in'][0]:
                            for outputs in ch.output:
                                if output.name == wire['in'][1]:
                                    if sl[0] == '':
                                        sl[0] = 1
                                    else:
                                        sl[0] = int(sl[0])
                                    if sl[1] == '':
                                        sl[1] = len(output)
                                    else:
                                        sl[1] = int(sl[1])
                                    pin1 = BusSlice(output, sl[0], sl[1])
                                    break
                else:
                    for ch in self.chips:
                        if ch.name == pin[0]:
                            for output in ch.outputs:
                                if output.name == pin[1]:
                                    pin_nr = int(pin[2])
                                    pin1 = output[pin_nr - 1]

            if '.' not in wire['out'] and '[' not in wire['out']:
                for output in self.outputs:
                    if output.name == wire['out']:
                        pin2 = output
                        break
            elif '[' not in wire['out']:
                wire_out = wire['out'].split('.')
                for ch in self.chips:
                    if ch.name == wire_out[0]:
                        for input in ch.inputs:
                            if input.name == wire_out[1]:
                                pin2 = input
                                break
                        break
            elif '.' not in wire['out']:
                pin = re.split(r'\[|\]', wire['out'])
                if ':' in pin[1]:
                    sl = pin[1].split(':')
                    for output in self.outputs:
                        if output.name == pin[0]:
                            if sl[0] == '':
                                sl[0] = 1
                            else:
                                sl[0] = int(sl[0])
                            if sl[1] == '':
                                sl[1] = len(output)
                            else:
                                sl[1] = int(sl[1])
                            pin2 = BusSlice(output, sl[0], sl[1])
                            break
                else:
                    for output in self.outputs:
                        if output.name == pin[0]:
                            pin_nr = int(pin[1])
                            pin2 = output[pin_nr - 1]
            else:
                pin = re.split(r'\[|\]|\.', wire['out'])
                if ':' in pin[2]:
                    sl = pin[2].split(':')
                    for ch in self.chips:
                        if ch.name == wire['out'][0]:
                            for input in ch.inputs:
                                if input.name == wire['out'][1]:
                                    if sl[0] == '':
                                        sl[0] = 1
                                    else:
                                        sl[0] = int(sl[0])
                                    if sl[1] == '':
                                        sl[1] = len(input)
                                    else:
                                        sl[1] = int(sl[1])
                                    pin2 = BusSlice(input, sl[0], sl[1])
                                    break
                else:
                    for ch in self.chips:
                        if ch.name == pin[0]:
                            for input in ch.inputs:
                                if input.name == pin[1]:
                                    pin_nr = int(pin[2])
                                    pin2 = input[pin_nr - 1]

            if hasattr(pin1, '__getitem__'):
                if len(pin1) == len(pin1):
                    for i in range(len(pin1)):
                        self.wires.append((pin1[i], pin2[i]))
                else:
                    raise Exception('Uneven buses')
            else:
                self.wires.append((pin1, pin2))
        # self.graph, self.user_graph = self.build_graph()

    def tick(self, inputs):
        pins = []
        for input in self.inputs:
            for name in inputs:
                if input.name == name:
                    if isinstance(input, Bus):
                        input.set_pins(inputs[name])
                        pins += input.pins
                    else:
                        input.value = inputs[name]
                        input.ticked = True
                        pins.append(input)
                    break
        for output in self.outputs:
            output.ticked = False
            pins.append(output)
        for chip in self.chips:
            for inp in chip.inputs:
                inp.ticked = False
                pins.append(inp)
            for out in chip.outputs:
                out.ticked = False
                if chip.code == 'DFF':
                    chip.update()
                    out.ticked = True
                pins.append(out)
        wires = []
        for wire in self.wires:
            wires.append(wire)

        while wires:
            done = []
            for index, wire in enumerate(wires):
                if wire[0].ticked:
                    wire[1].value = wire[0].value
                    wire[1].ticked = True
                    if all([pin.ticked for pin in wire[1].parent.inputs]) and wire[1].parent in self.chips:
                        ins = {}
                        for input in wire[1].parent.inputs:
                            ins[input.name] = input.value
                        wire[1].parent.tick(ins)
                        for output in wire[1].parent.outputs:
                            output.ticked = True
                    done.append(index)
            done.sort(reverse=True)
            for index in done:
                del wires[index]

    '''
    def build_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.chips)
        user_graph = nx.DiGraph()
        user_graph.add_nodes_from(self.chips)
        user_graph.add_nodes_from(self.inputs)
        user_graph.add_nodes_from(self.outputs)
        for wire in self.wires:
            if wire[0].parent.code == 'DFF':
                pass
            elif wire[0].parent is self or wire[1].parent is self:
                pin1 = wire[0].parent
                pin2 = wire[1].parent
                if pin1 is self:
                    pin1 = wire[0]
                if pin2 is self:
                    pin2 = wire[1]
                user_graph.add_edge(pin1, pin2)
            else:
                graph.add_edge(wire[0].parent, wire[1].parent)
                user_graph.add_edge(wire[0].parent, wire[1].parent)
        return graph, user_graph

    def show_graph(self):
        nx.draw_networkx(self.user_graph)
        plt.show()
    '''

    def parts_count(self):
        nand = 0
        dff = 0
        for chip in self.chips:
            in_nand, in_dff = chip.parts_count()
            nand += in_nand
            dff += in_dff
        return nand, dff

    def __str__(self):
        text = f'{self.name} {self.code}\n'
        for out in self.outputs:
            length = max(len(out.name), len(str(out.value))) + 2
            text += f'{out.name:>{length}}'
        text += '\n'
        for out in self.outputs:
            length = max(len(out.name), len(str(out.value))) + 2
            text += f'{str(out.value):>{length}}'
        return text


class NAND(Chip):

    def __init__(self, name):
        self.code = 'NAND'
        self.name = name
        self.description = 'NAND gate'
        self.inputs = [Pin('in1', self), Pin('in2', self)]
        self.outputs = [Pin('out', self)]
        self.chips = {}
        self.wires = []

    def tick(self, inputs):
        if inputs['in1'] and inputs['in2']:
            self.outputs[0].value = 0
        else:
            self.outputs[0].value = 1

    def parts_count(self):
        return 1, 0
    
    @classmethod
    def build(cls, name):
        return cls(name)


class DFF(Chip):

    def __init__(self, name):
        self.code = 'DFF'
        self.name = name
        self.description = 'Delay flip-flop'
        self.inputs = [Pin('in', self)]
        self.outputs = [Pin('out', self)]
        self.chips = {}
        self.wires = []
        self._value = 0

    def tick(self, inputs):
        self.outputs[0].value = self._value
        self._value = inputs['in']

    def update(self):
        self.outputs[0].value = self._value

    def parts_count(self):
        return 0, 1
    
    @classmethod
    def build(cls, name):
        return cls(name)


class Pin:

    def __init__(self, name, parent):
        self.name = name
        self.value = 0
        self.parent = parent
        self.ticked = False

    def __str__(self):
        return self.name


class Bus:

    def __init__(self, name, width, parent):
        self.name = name
        self.width = width
        self.parent = parent
        self.pins = []
        for i in range(width):
            self.pins.append(Pin(f'{name}[{i + 1}]', parent))

    def set_pins(self, values):
        for index, pin in enumerate(self.pins):
            pin.value = values[index]
            pin.ticked = True

    @property
    def ticked(self):
        return all(pin.ticked for pin in self.pins)

    @ticked.setter
    def ticked(self, value):
        for pin in self.pins:
            pin.ticked = value

    @property
    def value(self):
        return [pin.value for pin in self.pins]

    def __str__(self):
        return f'{self.name}[{self.width}]'

    def __getitem__(self, key):
        return self.pins[self.width - key - 1]

    def __len__(self):
        return self.width


class BusSlice:

    def __init__(self, bus, begin, end):
        self.bus = bus
        self.begin = begin
        self.end = end
        self.width = end - begin + 1

    def __str__(self):
        return f'{self.bus.name}[{self.begin}:{self.end}]'

    def __getitem__(self, item):
        return self.bus[self.begin + item - 1]

    def __len__(self):
        return self.width
