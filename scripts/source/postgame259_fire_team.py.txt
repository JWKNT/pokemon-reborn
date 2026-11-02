"""Prepare an owned trained Fire reserve through normal PC controls."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('FIRE TEAM',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame259-Will5-status.json').read_text());assert s['party'][0]['name']=='Amoonguss' and s['party'][0]['item']=='AMULETCOIN'
run('take_held','Amoonguss','Amulet Coin')
run('q','38,9,20,up:.12,c,wait:1');run('pc_open_reviewed')
run('pc_exchange_named',23,0,'Arcanine','Amoonguss')
run('checkpoint','Postgame259-FireTeam')
