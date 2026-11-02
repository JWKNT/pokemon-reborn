"""Prepare capture moves and factory switches through reviewed normal controls."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('teach_machine','TM54','Zeraora','False Swipe',0)
run('party_lead','Zapdos')
run('checkpoint','Genesect317-CaptureMoves')
for eid in [135,160,161,82]:
 run('eventq',877,eid,'talk')
 run('choose_dialog','Yes|No','Yes','--source',877,eid)
 run('dialog','--limit',12)
 run('checkpoint','Genesect317-Switch'+str(eid))
q=ROOT/'work/317-capture-route.json';q.write_text(json.dumps([[877,0,0,30,5,[]]]));run('queue_route',q)
run('checkpoint','Genesect317-PreCatch')
