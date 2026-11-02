"""Recover field-hazard damage using owned medicine before the boss."""
import os,sys,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(s,*a):
 print('FIELD HEAL',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
for name in ['Swampert','Sylveon','Amoonguss']:
 run('field_medicine','Full Restore',name);run('overworld')
for name in ['Zapdos','Aegislash','Mawile']:
 for _ in range(2):run('field_medicine','Ultra Potion',name);run('overworld')
run('party_lead','Aegislash')
run('checkpoint','Postgame251-SwordsHealed')
s=json.loads((R/'notes/Postgame251-SwordsHealed-status.json').read_text());assert all(m['hp']==m['totalhp'] for m in s['party'])
run('q','835,57,65');run('checkpoint','Postgame251-SwordsReady')
