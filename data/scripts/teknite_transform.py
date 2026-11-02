"""Use a reviewed field-changing move in a public wild battle, then exit normally."""
from play import *
import difflib
actor=sys.argv[1];slot=int(sys.argv[2]);dest=int(sys.argv[3]);label=sys.argv[4]
assert (actor,slot) in [('Ampharos',3),('Swampert',1)] and dest in [639,640,641,647,648,650]
t=read();rows=re.sub(r'\bHron\b','Aron',t).splitlines();names=['Carbink','Aron','Lairon'] if actor=='Ampharos' else ['Carbink','Aron','Lairon','Boldore','Gigalith','Dugtrio','Sandslash','Heatmor','Durant','Turtonator']
foes=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),z.strip().lower()).ratio()>.83 for z in rows)]
assert len(foes)==1 and 'fight' in t.lower(),('Public wild command review',t)
foe=foes[0];start=time.time()-5
p=ROOT/'notes/battle-control.json';ctl=json.loads(p.read_text());ctl['expected_foes']=foes;p.write_text(json.dumps(ctl))
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('battle_switch',actor)
if actor=='Swampert':run('public_turn_capture','battle_move.py',slot,'--watch')
else:run('battle_move',slot,'--watch')
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
 if any(z in lo for z in ['crystals','stones seem','fissures']):break
 if len(lo.replace('pokemon reborn','').strip())<8:
  blank+=1
  if blank>=2:break
 else:blank=0
 act('wait:.5')
else:raise SystemExit('Transformation tail timeout')
run('settle_arrival',dest)
if not fled:
 assert fainted,'No recorded faint for victory music'
 run('close_wild_music',foe)
run('checkpoint',label)
