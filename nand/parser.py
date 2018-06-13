import pathlib
import json
from nand.chip import ChipInfo
from nand.store import store


def to_dict(chip):
    d = {}
    sections = chip.split(';')
    for section in sections:
        section = section.strip()
        if section != '':
            section = section.split('\n')
            section = [line.strip() for line in section if line.strip() != '']
            if section[0] == 'Name' and len(section) == 2:
                d['Name'] = section[1]
            elif section[0] == 'Description' and len(section) > 1:
                d['Description'] = '\n'.join(section[1:])
            elif section[0] == 'Inputs':
                d['Inputs'] = []
                for line in section[1:]:
                    inputs = [inpt.strip() for inpt in line.split(',') if inpt.strip() != '']
                    for inpt in inputs:
                        d['Inputs'].append(inpt)
            elif section[0] == 'Outputs':
                d['Outputs'] = []
                for line in section[1:]:
                    outputs = [outpt.strip() for outpt in line.split(',') if outpt.strip() != '']
                    for outpt in outputs:
                        d['Outputs'].append(outpt)
            elif section[0] == 'Chips':
                d['Chips'] = []
                for line in section[1:]:
                    chips = [chip.strip() for chip in line.split(',') if chip.strip() != '']
                    chips = [chip.split() for chip in chips]
                    for chip in chips:
                        if len(chip) == 2:
                            ch = {'name': chip[0].strip(), 'type': chip[1].strip()}
                            d['Chips'].append(ch)
            elif section[0] == 'Wires':
                d['Wires'] = []
                for line in section[1:]:
                    wires = [wire.strip() for wire in line.split(',') if wire.strip() != '']
                    for wire in wires:
                        wire = [pin.strip() for pin in wire.split('->') if pin.strip() != '']
                        if len(wire) == 2:
                            w = {'in': wire[0].strip(), 'out': wire[1].strip()}
                            d['Wires'].append(w)
    return d


def load_chips():
    path = pathlib.Path('.')
    paths = list(path.glob('chips/*.chip'))
    data = []
    for path in paths:
        with open(path, 'r') as file:
            text = file.read()
            data.append(to_dict(text))

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
            break
