"""Two safe False Swipes, with public-HUD health checks before each action."""
from play import *
from public_owned_hp import read as owned_hp
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for _ in range(2):
 rows=snap();low=' '.join(r['text'] for r in rows).lower()
 assert 'genesect' in low and 'zeraora' in low and 'fight' in low and 'par' in low
 hp=owned_hp(rows,371);print('Observed Zeraora HP',hp,flush=True)
 if hp<180:
  run('battle_item','Ultra Potion','Zeraora');run('battle_ready')
  rows=snap();assert owned_hp(rows,371)>=180,'Review healing turn'
 run('battle_move',0,'--watch');run('battle_ready')
