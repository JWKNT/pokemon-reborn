from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('party_front','Zeraora')
for eid in [160,82]:
 run('eventq',877,eid,'talk')
 run('choose_dialog','Yes|No','Yes','--source',877,eid)
 run('dialog','--limit',12)
run('checkpoint','Genesect316-Heating')
q=ROOT/'work/316-aya-route.json'
run('queue_route',q)
run('play','up')
run('linear_dialog',877,33,'--source-page',5,'--burst')
run('checkpoint','Genesect316-AyaHot')
