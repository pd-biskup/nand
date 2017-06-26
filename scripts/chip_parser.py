from scripts import chip
from string import whitespace
import pathlib
import networkx as nx
from matplotlib import pyplot as plt


class Parser:

    _chips = {}

    def __init__(self):
        pass

    @staticmethod
    def chips():
        if not Parser._chips:
            Parser.parse()
        return Parser._chips

    @staticmethod
    def preparse():
        path = pathlib.Path('.')
        file_paths = list(path.glob('chips/*.chip'))

        result = []
        for file_path in file_paths:
            file = open(file_path, 'r')
            text = ''.join(file.readlines())
            file.close()
            sections = text.split(';')
            for i in range(len(sections)):
                sections[i] = sections[i].strip()
            if len(sections) is not 7:
                raise Exception('Sections parse error')
            if not sections[0].startswith('Name'):
                raise Exception('Section Name parse error')
            name = sections[0][4:].strip()
            if any(char in name for char in whitespace) or not name.isalnum():
                raise Exception('Name parse error')
            if not sections[1].startswith('Description'):
                raise Exception('Section Description parse error')
            description = sections[1][11:].strip()
            if not sections[2].startswith('Inputs'):
                raise Exception('Section Inputs parse error')
            inputs = sections[2][6:].replace('\n', '').split(',')
            for i in range(len(inputs)):
                inputs[i] = inputs[i].strip()
                if any(char in inputs[i] for char in whitespace) or not inputs[i].isalnum():
                    raise Exception('Input parse error: %s')
            if not sections[3].startswith('Outputs'):
                raise Exception('Section Outputs parse error')
            outputs = sections[3][7:].replace('\n', '').split(',')
            for i in range(len(outputs)):
                outputs[i] = outputs[i].strip()
                if any(char in outputs[i] for char in whitespace) or not outputs[i].isalnum():
                    raise Exception('Output parse error')
            if not sections[4].startswith('Chips'):
                raise Exception('Section Chips parse error')
            chips = sections[4][5:].replace('\n', '').split(',')
            for i in range(len(chips)):
                chips[i] = chips[i].strip().split(' ')
                for j in range(len(chips[i])):
                    chips[i][j] = chips[i][j].strip()
                if len(chips[i]) is not 2\
                        or any(char in chips[i][0] for char in whitespace) or not chips[i][0].isalnum()\
                        or any(char in chips[i][1] for char in whitespace) or not chips[i][0].isalnum():
                    raise Exception('Chips parse error')
            if not sections[5].startswith('Wires'):
                raise Exception('Section Wires parse error')
            wires = sections[5][5:].replace('\n', '').split(',')
            for i in range(len(wires)):
                wires[i] = wires[i].split('->')
                for j in range(len(wires[i])):
                    wires[i][j] = wires[i][j].strip()
                if len(wires[i]) is not 2\
                        or any(char in wires[i][0] for char in whitespace)\
                        or any(char in wires[i][1] for char in whitespace):
                    raise Exception('Wires parse error')
            dependencies = set()
            for ch in chips:
                dependencies.add(ch[1])
            result.append((name, dependencies, (name, description, inputs, outputs, chips, wires)))
        return result

    @staticmethod
    def build_graph(chips):
        graph = nx.DiGraph()
        graph.add_node('NAND')
        graph.add_nodes_from([ch[0] for ch in chips])
        for ch in chips:
            for dep in ch[1]:
                graph.add_edge(ch[0], dep)
        try:
            nx.find_cycle(graph)
        except nx.NetworkXNoCycle:
            pass
        else:
            raise Exception('Dependency error')
        # nx.draw_networkx(graph)
        # plt.show()
        return graph

    @staticmethod
    def parse():
        data = Parser.preparse()
        graph = Parser.build_graph(data)
        for chunk in data:
            Parser._chips[chunk[0]] = chunk[2]
