"""Complete the reviewed Diancie capture and Cain return through ordinary UI."""
import os, subprocess, sys, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(name,*args):
 print('DIANCIE RETURN',name,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True)
run('finish_capture','Diancie')
run('close_wild_music','Diancie','--since',1791722470,'--battle-track','Battle- Legendary')
run('checkpoint','Diancie293-Caught')
run('eventq',860,130,'item')
run('eventq',860,7,'enter')
# Exit lands beside Cain and automatically starts his reviewed return scene.
run('dialog','--yes','--limit=100','--story-burst')
run('checkpoint','Diancie293-QuestDone')
s=json.loads((R/'notes/Diancie293-QuestDone-status.json').read_text())
assert s['map']==826,s['map']
print('DIANCIE QUEST RETURN VERIFIED',flush=True)
