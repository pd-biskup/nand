import pathlib
import json
from nand.chip import ChipInfo
from nand.store import store


def load_chips():
    path = pathlib.Path('.')
    paths = list(path.glob('chips/*.json'))
    data = []
    for path in paths:
        with open(path, 'r') as file:
            json_data = json.load(file)
            data.append(json_data)

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
