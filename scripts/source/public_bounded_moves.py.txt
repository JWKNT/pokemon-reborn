"""Execute a finite move plan while the public matchup and HP stay within reviewed bounds."""
from play import *
from public_owned_hp import read as hp_read
import argparse,difflib
p=argparse.ArgumentParser();p.add_argument('actor');p.add_argument('foe');p.add_argument('maxhp',type=int);p.add_argument('minhp',type=int);p.add_argument('moves');p.add_argument('journal',type=pathlib.Path);a=p.parse_args()
slots=[int(x)for x in a.moves.split(',')];assert 1<=len(slots)<=5 and all(0<=x<=3 for x in slots);assert not a.journal.exists()
d={'plan':slots,'events':[],'status':'running'}
def save():a.journal.write_text(json.dumps(d,indent=2))
try:
 for slot in slots:
  rows=snap();t=' '.join(x['text']for x in rows).lower()
  enemy=' '.join(x['text'].lower() for x in rows if x['y']<.37)
  foe_seen=any(difflib.SequenceMatcher(None,a.foe.lower(),w.strip('.,')).ratio()>=.78 for w in enemy.split())
  # Recorded Mew HUDs can OCR the final w as Cyrillic sh; keep whole-word matching.
  actor_text=t.translate(str.maketrans({'ш':'w','е':'e'}))
  actor_names=[a.actor.lower()]+(['meurtwo','mewrtwo','mewtuo','meurtuo'] if a.actor.lower()=='mewtwo' else [])
  actor_seen=any(re.search(r'\b'+re.escape(name)+r'\b',actor_text) for name in actor_names)
  assert actor_seen and foe_seen and 'fight' in t and 'run' in t,t
  assert not re.search(r'\b(?:frz|slp|par|frozen|asleep|paralyzed)\b',t),'Status requires public review: '+t
  hp=hp_read(rows,a.maxhp);assert hp>=a.minhp,(hp,a.minhp)
  e=dict(slot=slot,hp=hp,epoch=time.time(),pending=True);d['events'].append(e);save();print('GUARDED MOVE',e,flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),str(slot),'--watch'],check=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
  e['pending']=False;save()
 d['status']='completed';save()
except Exception:
 d['status']='inspect_public_state_before_any_resume';save();raise
