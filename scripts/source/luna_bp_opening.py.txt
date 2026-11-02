"""Reviewed Luna Fairy Tale opening using normal UI and public command guards."""
from play import *
def run(s,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
run('glass_turn','work/241-luna-screens.json')
t=read().lower()
if 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):run('party_pick','Mawile')
elif 'fight' in t and 'hexan' in t:run('battle_switch','Mawile');run('battle_ready')
else:raise SystemExit('Opening replacement screen needs review: '+t)
run('glass_turn','work/241-luna-dance.json')
run('battle_batch','Mawile',1,'--foes','HumptyDumpty,KnaveOfHearts,Snark,Jabberwocky','--foe-slots',json.dumps({'humptydumpty':1,'knaveofhearts':1,'snark':2,'jabberwocky':1}),'--turns',5,'--stay','--stay-team-reviewed','--stop-foes','Carpenter,Rabbit','--min-hp',.25,'--watch')
