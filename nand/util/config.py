from enum import IntEnum
from sys import stdout


class Level(IntEnum):
    ERR = 0
    WRN = 1
    INF = 2
    DBG = 3

workspace = '~/.nand'

log_level = Level.ERR
log_output = [stdout]

color = False
colors = {
    'default': '\033[0m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m'
}