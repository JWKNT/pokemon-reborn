"""Leave after the caught Genesect and view source-reviewed aftermath scenes."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for eid in [152,161]:
 run('eventq',877,eid,'talk');run('choose_dialog','Yes|No','Yes','--source',877,eid);run('dialog','--limit',12);run('checkpoint','Genesect317-Removed'+str(eid))
run('eventq',877,1,'enter')
run('eventq',596,15,'talk');run('linear_dialog',596,15,'--source-page',1,'--burst')
run('checkpoint','Genesect317-AyaAftermath')
run('genesect317_lin_exit')
