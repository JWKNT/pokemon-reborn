"""Four-turn normal-input Perish Song plan; adapts only to visible KO/command state."""
from play import *
import difflib
def r(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
def ready():r('battle_ready');return read().lower()
def party(t):return 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5)
def won(t):return bool(re.search(r'de.?feated|for winning',t))
t=read().lower();assert 'fight'in t
if '--resume-turn' in sys.argv:
 turn=int(sys.argv[sys.argv.index('--resume-turn')+1]);assert 1<=turn<=3
else:
 assert 'kricketune'in t or 'krickertune'in t
 r('battle_move',3,'--watch');t=ready();turn=1
while turn<4 and not won(t):
 if party(t):
  # Kricketune KO first/second turn, or sacrificial Cofagrigus KO third.
  r('party_pick','Swampert');t=ready()
 assert 'fight'in t and 'reshiram'in t,'Unexpected dragon command '+t
 prompt=t.split('what')[-1] if 'what' in t else t
 def actor(name):return any(difflib.SequenceMatcher(None,name,w.strip('.,?!')).ratio()>.78 for w in prompt.split())
 if actor('kricketune'):
  r('battle_move',0,'--watch')
 elif actor('swampert'):
  if turn in [1,3]:r('battle_move',3,'--watch')
  else:r('battle_switch','Cofagrigus')
 elif actor('cofagrigus'):
  # If the switch-in survived turn3, a neutral status action burns the last turn.
  assert turn==3;r('battle_move',0,'--watch')
 else:raise SystemExit('Reviewed actor not visible: '+prompt)
 turn+=1;t=ready()
assert won(t),'Need observed four-turn Perish victory: '+t
print('DRAGON PERISH VICTORY',turn,flush=True)
