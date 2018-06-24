from enum import IntEnum
from sys import stdout


class Level(IntEnum):
    NON = 0
    ERR = 1
    WRN = 2
    INF = 3
    DBG = 4

workspace = '~/.nand'

log_level = Level.DBG
log_output = [stdout]

color = True
colors = {
    'default': '\033[0m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m'
}