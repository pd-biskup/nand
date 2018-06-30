import json
import os
import pathlib
import glob
from nand.core.chip import ChipInfo
from nand.core.store import store
from nand.core.test import Test
from nand.util.log import log
import nand.util.config as config


def parse_chip(chip):
    d = {}
    sections = parse_sections(chip)
    for name, content in sections.items():
        if name == 'Name':
            d['Name'] = content
        elif name == 'Description':
            d['Description'] = content
        elif name == 'Inputs':
            d['Inputs'] = []
            for line in content.split('\n'):
                inputs = [inpt.strip() for inpt in line.split(',') if inpt.strip() != '']
                for inpt in inputs:
                    d['Inputs'].append(inpt)
        elif name == 'Outputs':
            d['Outputs'] = []
            for line in content.split('\n'):
                outputs = [outpt.strip() for outpt in line.split(',') if outpt.strip() != '']
                for outpt in outputs:
                    d['Outputs'].append(outpt)
        elif name == 'Chips':
            d['Chips'] = []
            for line in content.split('\n'):
                chips = [chip.strip() for chip in line.split(',') if chip.strip() != '']
                chips = [chip.split() for chip in chips]
                for chip in chips:
                    if len(chip) == 2:
                        ch = {'name': chip[0].strip(), 'type': chip[1].strip()}
                        d['Chips'].append(ch)
        elif name == 'Wires':
            d['Wires'] = []
            for line in content.split('\n'):
                wires = [wire.strip() for wire in line.split(',') if wire.strip() != '']
                for wire in wires:
                    wire = [pin.strip() for pin in wire.split('->') if pin.strip() != '']
                    if len(wire) == 2:
                        w = {'in': wire[0].strip(), 'out': wire[1].strip()}
                        d['Wires'].append(w)
    return d


def parse_test(test):
    sections = parse_sections(test)
    for section, content in sections.items():
        if section == 'Name':
            name = content
        elif section == 'Description':
            description = content
        elif section == 'Chip':
            chip = content
        elif section == 'Test':
            test = {}
            labels = content.split('\n')[0].split()
            for label in labels:
                test[label] = []
            for values in content.split('\n')[1:]:
                values = values.split()
                if len(values) == len(labels):
                    for i in range(len(labels)):
                        if len(values[i]) == 1:
                            test[labels[i]].append(int(values[i]))
                        else:
                            test[labels[i]].append([])
                            for bit in values[i]:
                                test[labels[i]][-1].append(int(bit))
    t = Test(name, description, chip, test)
    return t


def load_file(path):
    with open(path, 'r') as file:
        text = file.read()
        return text


def parse_sections(text):
    split = text.split(';')
    sections = {}
    for section in split:
        section = section.strip()
        if section != '':
            lines = section.split('\n')
            name = lines[0].strip()
            content = '\n'.join(lines[1:]).strip()
            sections[name] = content
    return sections


def load_chips():
    log.log('Loading chips', config.Level.INF)
    path = os.path.expanduser(os.path.join(config.workspace, 'chips/**/*.chip'))
    paths = glob.glob(path, recursive=True)
    data = []
    for path in paths:
        data.append(parse_chip(load_file(path)))

    while len(data) > 0:
        length = len(data)
        for i in range(len(data)):
            if all([ch['type'] in store for ch in data[i]['Chips']]):
                store.register(data[i]['Name'],
                               ChipInfo(data[i]['Name'], data[i]['Description'],
                                        data[i]['Inputs'], data[i]['Outputs'], data[i]['Chips'],
                                        data[i]['Wires']))
                del data[i]
                break
        if length == len(data):
            log.log('Some chips have unresolved dependencies', config.Level.WRN)
            break
    log.log(f'Loaded {len(store)} chips', config.Level.INF)


def load_test(name):
    log.log(f'Loading test: {name}', config.Level.DBG)
    path = pathlib.Path(os.path.expanduser(os.path.join(config.workspace, f'tests/{name}.test')))
    if path.exists():
        text = load_file(path)
        test = parse_test(text)
        log.log(f'Loaded test: {name}', config.Level.DBG)
        return test
    else:
        log.log(f'Loading test failed. File {path.absolute()} not found.', config.Level.ERR)
        raise FileNotFoundError(path.absolute())
