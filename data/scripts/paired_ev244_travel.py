"""Known city route to the Railnet training strip; stay inside connected-map edges."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
e=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,args)],env=e,check=True)
# Expected start: Opal Fly landing after preparing both held items and Walrein lead.
# Recorded244 arrivals established the connected-map boundary tiles:
# 519[9,60] precedes530; short route overshoot can cross early. Two bounded exit taps cover the observed edge tolerance.
run('q','519,10,60,left:.12,left:.12,wait:2','530,94,13,right:.12,wait:2','519,29,11,right:.12,wait:2','513,14,8,right:.12,right:.12,wait:2','519,58,11,right:.12,wait:2','633,10,8')
run('paired_ev244','ready')
