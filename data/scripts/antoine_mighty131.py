"""One reviewed switch decline, then finite burn and guaranteed Hex finish."""
import json,subprocess,sys
from play import ROOT,read,act
t=read().lower();assert 'yes' in t and 'no' in t and 'change' in t
act('x:.12','wait:.7')
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
base=[sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Mightyena']
def one(tag,action,hp):
 path='work/antoine-mighty-'+tag+'131.json'
 rc=subprocess.run(base+action+['--min-hp',str(hp),'--output',path]).returncode
 r=json.loads((ROOT/path).read_text());assert rc==0,r.get('error',r.get('final_guard_stop'))
 return r
r=one('burn',['--move-slot','2'],100)
assert any('was burned' in ' '.join(s['text']).lower() for s in r['public_screens'])
if r['final_hp_proof']['hp']<90:
 r=one('heal',['--item','Ultra Potion'],1);assert r['final_hp_proof']['hp']>=90
one('hex',['--move-slot','1'],90)
