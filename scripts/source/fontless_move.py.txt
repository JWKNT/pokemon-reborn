"""One manually reviewed Terra move via normal keys; public command guard only.

No live game/save/battle-log reads. Caller identifies sprites and desired slot
from the rendered screen and frozen entry roster. Stops after this one turn.
"""
import sys,json,time
from play import ROOT,act,read
slot=int(sys.argv[1]);assert 0<=slot<4
music=json.loads((ROOT/'work/active-trainer-music.json').read_text())
assert (music['class'],music['name'],str(music['map']))==('TERRA','T3RR4','778')
t=read().lower();assert 'fight' in t and ('bag' in t or 'bae' in t) and 'run' in t,'Public command screen required'
act('left:.12','up:.12','c','wait:.3','left:.12','up:.12',*(['right:.12'] if slot%2 else []),*(['down:.12'] if slot//2 else []),'c','wait:5')
print(read(),flush=True)
