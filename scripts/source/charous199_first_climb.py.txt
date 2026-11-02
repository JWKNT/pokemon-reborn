"""Trigger the reviewed first Charous story climb from its public coordinate."""
from play import *
from locate import locate
assert locate(792)==(792,25,50)
act('right:.18','c','wait:1');print(read(),flush=True)
