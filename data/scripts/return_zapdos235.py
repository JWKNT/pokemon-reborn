"""Recorded normal healing and reviewed route to the pre-Zapdos checkpoint."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_ROUTE_CHUNK='84',REBORN_COORD_CACHE='1')
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
m=next(m for m in json.loads((R/'notes/Postgame235-AmooBulk-status.json').read_text())['party'] if m['species']=='AMOONGUSS')
assert m['ev']==[252,0,252,0,0,0]
run('fly_to',519,'--carrier','Altaria');run('eventq',519,116,'enter');run('eventq',38,3,'talk');run('heal');run('eventq',38,6,'enter')
run('party_front','Hexan');run('fly_to',525,'--carrier','Altaria')
run('connected_walk',525,543,9,10);run('connected_walk',543,560,23,11)
run('eventq',560,5,'enter');run('q','197,9,7');run('checkpoint','Postgame235-ZapdosReady')
s=json.loads((R/'notes/Postgame235-ZapdosReady-status.json').read_text())
assert all(m['hp']==m['totalhp'] for m in s['party'])
a=next(m for m in s['party'] if m['species']=='AMOONGUSS');assert a['item'] is None,(a['item'])
assert s['bag']['contents']['TIMERBALL']==30
print('ZAPDOS PREPARATION VERIFIED',a['totalhp'],a['defense'],flush=True)
