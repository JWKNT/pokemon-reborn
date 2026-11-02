from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for eid in [135,152]:
 run('eventq',877,eid,'talk')
 run('choose_dialog','Yes|No','Yes','--source',877,eid)
 run('dialog','--limit',12)
run('checkpoint','Genesect316-Cooling')
q=ROOT/'work/316-aya-route.json';q.write_text(json.dumps([[877,0,0,30,48,[]]]))
run('queue_route',q)
run('play','up')
run('linear_dialog',877,33,'--source-page',3,'--burst')
run('checkpoint','Genesect316-AyaCold')
