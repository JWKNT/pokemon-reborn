"""Bounded Magearna sweep from public HUD, with explicit stay-in choices and HP stop."""
from play import *
from public_owned_hp import read as hp_read
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
p=ROOT/'work/304-sweep-journal.json';assert not p.exists()
d={'events':[],'status':'running'}
def save():p.write_text(json.dumps(d,indent=2))
def run(n,*a):return subprocess.run([sys.executable,str(ROOT/'scripts'/f'{n}.py'),*map(str,a)],check=True)
try:
 for i in range(9):
  ready=subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')])
  rows=snap();t=' '.join(r['text']for r in rows).lower()
  if 'de' in t and re.search(r'de.?feated|for winning',t):d['status']='victory';save();break
  if 'change pok' in t and 'yes' in t and 'no' in t:
   run('choose_dialog','Yes|No','No');run('battle_ready');rows=snap();t=' '.join(r['text']for r in rows).lower()
  else:assert ready.returncode==0,t
  assert 'magearna' in t and 'fight' in t and 'run' in t,t
  hp=hp_read(rows,452);assert hp>=120,('HP review',hp)
  enemy=' '.join(r['text']for r in rows if r['y']<.37).lower()
  match=[(name,slot)for name,slot in [('sylveon',0),('milotic',2),('azumarill',2),('magearna',0),('fini',2)]if name in enemy];assert len(match)==1,enemy
  name,slot=match[0];e=dict(epoch=time.time(),foe=name,hp=hp,slot=slot,pending=True);d['events'].append(e);save();print('SWEEP ACTION',e,flush=True)
  run('battle_move',slot,'--watch');e['pending']=False;save()
 else:d['status']='action_bound_reached';save()
except Exception:
 d['status']='inspect_before_resume';save();raise
