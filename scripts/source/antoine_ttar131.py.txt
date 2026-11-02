"""Finite root-reviewed Tyranitar heal, burn and two guaranteed finishing Hexes."""
import json,subprocess,sys
from play import ROOT
base=[sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute','--mode','antoine','--foes','Tyranitar']
def one(tag,action,hp):
 path='work/antoine-ttar-'+tag+'131.json'
 rc=subprocess.run(base+action+['--min-hp',str(hp),'--output',path]).returncode
 r=json.loads((ROOT/path).read_text());assert rc==0,r.get('error',r.get('final_guard_stop'))
 return r
r=one('heal',['--item','Ultra Potion'],1)
assert r['final_hp_proof']['hp']>=120,'Actual postheal HP insufficient; stop before burn'
r=one('burn',['--move-slot','2'],120)
assert any('burn' in ' '.join(s['text']).lower() for s in r['public_screens']),'No visible burn proof; stop'
if r['final_hp_proof']['hp']<120:
 r=one('heal-before-hex',['--item','Ultra Potion'],1)
 assert r['final_hp_proof']['hp']>=120
r=one('hex-first',['--move-slot','1'],120)
assert r['final_classification']=='fresh_expected_command'
# Source no healing item / no priority. +6 speed272>139; burn Hex minimum171
# versus original301 means the second is a guaranteed KO before retaliation.
one('hex-finish',['--move-slot','1'],16)
