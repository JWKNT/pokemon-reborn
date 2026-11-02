"""Bounded two-turn normal-control opening, gated on the visible named matchup."""
from play import *
def expect():
 t=re.sub('[^a-z]','',read().lower())
 assert 'whatwillhexando' in t and 'starmie' in t,('Expected Hexan versus Starmie; no action selected',t)
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*args],check=True)
expect();run('battle_move','0','--watch');run('battle_ready')
expect();run('battle_move','3','--watch');run('battle_ready')
print('LIGHT SCREEN / FREEZE-DRY OPENING COMPLETE; inspect public HP and next foe',flush=True)
