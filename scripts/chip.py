import networkx as nx
from matplotlib import pyplot as plt
import copy


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
                self.inputs.append(Pin(input, self))
            self.outputs = []
            for output in data[3]:
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
                if '.' not in wire[0]:
                    for input in self.inputs:
                        if input.name == wire[0]:
                            pin1 = input
                            break
                else:
                    wire[0] = wire[0].split('.')
                    for ch in self.chips:
                        if ch.name == wire[0][0]:
                            for output in ch.output:
                                if output.name == wire[0][1]:
                                    pin1 = output
                                    break
                            break
                if '.' not in wire[1]:
                    for output in self.outputs:
                        if output.name == wire[1]:
                            pin2 = output
                            break
                else:
                    wire[1] = wire[1].split('.')
                    for ch in self.chips:
                        if ch.name == wire[1][0]:
                            for input in ch.input:
                                if input.name == wire[1][1]:
                                    pin2 = input
                                    break
                            break
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

    def tick(self, inputs):
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
                                wires_queue[wire] = True

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


class Pin:

    def __init__(self, name, parent):
        self.name = name
        self.value = False
        self.parent = parent

    def __str__(self):
        return self.name
