"""Queue the reviewed Ace opening; stop before the next uncertain opponent.

Uses fresh visible UI for every opponent gate, and never edits game state.
"""
from play import *
def run(n,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(n+'.py')),*map(str,args)],check=True)
def offered():
 t=read().lower();assert 'change pok' in t, 'Expected replacement offer: '+t
 rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()]
 return next(' '.join(r['text']).lower() for r in reversed(rows) if time.time()-r['epoch']<90 and 'about to send' in ' '.join(r['text']).lower())
t=read().lower()
assert 'fight' in t and 'roserade' in t, 'Expected Ace first command / Roserade'
run('battle_batch','Arcanine',1,'--foes','Roserade','--turns',1,'--watch')
incoming=offered()
if 'nidoqueen' in incoming:
 run('switch_offered','Nidoqueen','Hexan')
 run('battle_batch','Hexan',1,'--foes','Nidoqueen','--turns',2,'--watch')
 incoming=offered()
assert 'delphox' in incoming, 'Unexpected reviewed opening order: '+incoming
run('switch_offered','Delphox','Swampert')
run('battle_batch','Swampert',0,'--foes','Delphox','--turns',1,'--watch')
t=read().lower()
assert 'cancel' in t and t.count('hp')>=5 and ('choose a pok' in t or 'swampert' in t), 'Mandatory replacement requires review'
run('party_pick','Cofagrigus')
print('FRESH COFAGRIGUS ENTERED; VERIFY ILLUSION BEFORE CHOOSING ANY MOVE',flush=True)
