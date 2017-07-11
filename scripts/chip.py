import networkx as nx
from matplotlib import pyplot as plt
import copy
import re


class Chip:

    def __init__(self, name, code):
        self.name = name
        if code == 'NAND':
            self.code = code
            self.description = 'NAND gate'
            self.inputs = [Pin('in1', self), Pin('in2', self)]
            self.outputs = [Pin('out', self)]
            self.chips = {}
            self.wires = []
        elif code == 'DFF':
            self.code = code
            self.description = 'Delay flip-flop'
            self.inputs = [Pin('in', self)]
            self.outputs = [Pin('out', self)]
            self.chips = {}
            self.wires = []
        else:
            import scripts.chip_parser as parser
            data = copy.deepcopy(parser.Parser.chips()[code])
            self.code = data[0]
            self.description = data[1]
            self.inputs = []
            for input in data[2]:
                if input[-1] == ']':
                    bus = re.split(r'\[|\]', input)
                    count = int(bus[1])
                    self.inputs.append(Bus(bus[0], count, self))
                else:
                    self.inputs.append(Pin(input, self))
            self.outputs = []
            for output in data[3]:
                if output[-1] == ']':
                    bus = re.split(r'\[|\]', output)
                    count = int(bus[1])
                    self.outputs.append(Bus(bus[0], count, self))
                else:
                    self.outputs.append(Pin(output, self))
            self.chips = []
            for ch in data[4]:
                if ch[1] == 'NAND':
                    self.chips.append(NAND(ch[0]))
                elif ch[1] == 'DFF':
                    self.chips.append(DFF(ch[0]))
                else:
                    self.chips.append(Chip(ch[0], ch[1]))
            self.wires = []
            for wire in data[5]:
                pin1 = None
                pin2 = None

                if '.' not in wire[0] and '[' not in wire[0]:
                    for input in self.inputs:
                        if input.name == wire[0]:
                            pin1 = input
                            break
                elif '[' not in wire[0]:
                    wire[0] = wire[0].split('.')
                    for ch in self.chips:
                        if ch.name == wire[0][0]:
                            for output in ch.output:
                                if output.name == wire[0][1]:
                                    pin1 = output
                                    break
                            break
                elif '.' not in wire[0]:
                    pin = re.split(r'\[|\]', wire[0])
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
                    pin = re.split(r'\[|\]', wire[0])
                    if ':' in pin[1]:
                        sl = pin[1].split(':')
                        for ch in self.chips:
                            if ch.name == wire[0][0]:
                                for output in ch.output:
                                    if output.name == wire[0][1]:
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
                            if ch.name == wire[0][0]:
                                for output in ch.output:
                                    if output.name == wire[0][1]:
                                        pin_nr = int(pin[1])
                                        pin1 = output[pin_nr - 1]

                if '.' not in wire[1] and '[' not in wire[1]:
                    for output in self.outputs:
                        if output.name == wire[1]:
                            pin2 = output
                            break
                elif '[' not in wire[1]:
                    wire[1] = wire[1].split('.')
                    for ch in self.chips:
                        if ch.name == wire[1][0]:
                            for input in ch.input:
                                if input.name == wire[1][1]:
                                    pin2 = input
                                    break
                            break
                elif '.' not in wire[0]:
                    pin = re.split(r'\[|\]', wire[1])
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
                    pin = re.split(r'\[|\]', wire[1])
                    if ':' in pin[1]:
                        sl = pin[1].split(':')
                        for ch in self.chips:
                            if ch.name == wire[1][0]:
                                for input in ch.input:
                                    if input.name == wire[1][1]:
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
                            if ch.name == wire[1][0]:
                                for input in ch.input:
                                    if input.name == wire[1][1]:
                                        pin_nr = int(pin[1])
                                        pin2 = input[pin_nr - 1]

                if hasattr(pin1, '__getitem__'):
                    if len(pin1) == len(pin1):
                        for i in range(len(pin1)):
                            self.wires.append((pin1[i], pin2[i]))
                    else:
                        raise Exception('Uneven buses')
                else:
                    self.wires.append((pin1, pin2))
        self.graph, self.user_graph = self.build_graph()

    @property
    def input(self):
        return self.inputs

    @property
    def output(self):
        return self.outputs

    '''def tick(self, inputs):
        for name in inputs:
            for inpt in self.input:
                if name == inpt.name:
                    inpt.value = inputs[name]
                    break
        graph = nx.DiGraph()
        graph.add_nodes_from(self.graph.nodes())
        graph.add_edges_from(self.graph.edges())
        while len(graph.nodes()) > 0:
            queue = []
            for node in graph.nodes():
                if len(graph.predecessors(node)) is 0:
                    queue.append(node)
                    graph.remove_node(node)
            for chip in queue:
                ins = {}
                for wire in self.wires:
                    if wire[1].parent is chip:
                        ins[wire[1].name] = wire[0].value
                chip.tick(ins)
        for out in self.output:
            for wire in self.wires:
                if wire[1].parent is self and wire[1].name == out.name:
                    out.value = wire[0].value'''

    '''def tick(self, inputs):
        for name in inputs:
            for inpt in self.input:
                if name == inpt.name:
                    inpt.value = inputs[name]
                    break
        wires_queue = {}
        for wire in self.wires:
            if wire[0].parent is self or wire[0].parent.code == 'DFF':
                wires_queue[wire] = True
            else:
                wires_queue[wire] = False
        while len(wires_queue) > 0:
            for wire in wires_queue:
                if wires_queue[wire]:
                    wire[1].value = wire[0].value
                    chip = wire[1].parent
                    wires_queue[wire] = None
                    do_tick = True
                    for wire in wires_queue:
                        if chip is wire[1].parent and wires_queue[wire] is not None:
                            do_tick = False
                            break
                    if do_tick:
                        ins = {}
                        for input in chip.input:
                            ins[input.name] = input.value
                        chip.tick(ins)
                        for wire in wires_queue:
                            if chip is wire[0].parent and wires_queue[wire] is not None:
                                wires_queue[wire] = True'''

    def tick(self, inputs):
        pins = []
        for input in self.input:
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
        for output in self.output:
            output.ticked = False
            pins.append(output)
        for chip in self.chips:
            for inp in chip.input:
                inp.ticked = False
                pins.append(inp)
            for out in chip.output:
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
                    if all([pin.ticked for pin in wire[1].parent.input]) and wire[1].parent in self.chips:
                        ins = {}
                        for input in wire[1].parent.input:
                            ins[input.name] = input.value
                        wire[1].parent.tick(ins)
                        for output in wire[1].parent.output:
                            output.ticked = True
                    done.append(index)
            done.sort(reverse=True)
            for index in done:
                del wires[index]

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

    def __str__(self):
        return self.name


class NAND(Chip):

    def __init__(self, name):
        super().__init__(name, 'NAND')

    def tick(self, inputs):
        if inputs['in1'] and inputs['in2']:
            self.outputs[0].value = False
        else:
            self.outputs[0].value = True


class DFF(Chip):

    def __init__(self, name):
        super().__init__(name, 'DFF')
        self._value = False

    def tick(self, inputs):
        self.outputs[0].value = self._value
        self._value = bool(inputs['in'])

    def update(self):
        self.outputs[0].value = self._value


class Pin:

    def __init__(self, name, parent):
        self.name = name
        self.value = False
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
            self.pins.append(Pin('%s[%i]' % (name, i + 1), parent))

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
        return '%s[%i]' % (self.name, self.width)

    def __getitem__(self, item):
        return self.pins[item]

    def __len__(self):
        return self.width


class BusSlice:

    def __init__(self, bus, begin, end):
        self.bus = bus
        self.begin = begin
        self.end = end
        self.width = end - begin + 1

    def __str__(self):
        return '%s[%i:%i]' % (self.bus.name, self.begin, self.end)

    def __getitem__(self, item):
        return self.bus[self.begin + item - 1]

    def __len__(self):
        return self.width
