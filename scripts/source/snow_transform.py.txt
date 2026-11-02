"""Melt a reviewed snow/ice field using owned Chatot Heat Wave through normal controls."""
from play import *
import difflib
actor=sys.argv[1];slot=int(sys.argv[2]);dest=int(sys.argv[3]);label=sys.argv[4]
assert (actor,slot)==('Chatot',0) and dest in [719,750]
t=read();rows=re.sub(r'\bHron\b','Aron',t).splitlines();names=['Audino','Chansey','Hypno','Noctowl','Chimecho','Beartic','Sealeo','Avalugg','Sandslash','Glalie','Froslass','Walrein','Crabominable','Absol']
foes=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),z.strip().lower()).ratio()>.83 for z in rows)]
assert len(foes)==1 and 'fight' in t.lower(),('Public wild command review',t)
foe=foes[0];start=time.time()-5
p=ROOT/'notes/battle-control.json';ctl=json.loads(p.read_text());ctl['expected_foes']=foes;p.write_text(json.dumps(ctl))
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
if '--already-active' in sys.argv:
 assert any(difflib.SequenceMatcher(None,actor.lower(),z.strip().lower()).ratio()>.78 for z in rows), 'Active actor public name required'
else:run('battle_switch',actor)
run('public_turn_capture','battle_move.py',slot,'--watch')
fainted=any(r['epoch']>=start and 'fainted' in ' '.join(r['text']).lower() for r in [json.loads(z) for z in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]);fled=False;blank=0
for capture in (ROOT/'work').glob('public-turn-*/text.json'):
 if capture.stat().st_mtime>=start:
  fainted=fainted or any('fainted' in z['text'].lower() for z in json.loads(capture.read_text()))
for i in range(24):
 t=read();lo=t.lower();print(t,flush=True)
 if 'fight' in lo:
  run('flee','--since',json.loads((ROOT/'recordings'/('session-%03d.json'%json.loads((ROOT/'notes/current-run-control.json').read_text())['session'])).read_text())['start_epoch']);fled=True;break
 if 'fainted' in lo:fainted=True
 if any(z in lo for z in ['choose a pok','out of usable','trying to learn']):raise SystemExit('Battle outcome requires review')
 if any(z in lo for z in ['fainted','gained','exp. point','experience']):act('c','wait:.5');continue
 if any(z in lo for z in ['crystals','stones seem','fissures','thawed','melted','ice collapsed','water gushed']):break
 if len(lo.replace('pokemon reborn','').strip())<8:
  blank+=1
  if blank>=2:break
 else:blank=0
 act('wait:.5')
else:raise SystemExit('Transformation tail timeout')
t=read().lower()
if (dest==719 and 'snowpack thawed out' in t) or (dest==750 and any(z in t for z in ['icy basin thawed out','icy basin thaued out'])):act('c','wait:3')
run('settle_arrival',dest)
if not fled:
 assert fainted,'No recorded faint for victory music'
 run('close_wild_music',foe)
run('checkpoint',label)
