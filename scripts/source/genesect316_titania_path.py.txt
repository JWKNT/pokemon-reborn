from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
for eid in [123,93]:
 run('eventq',877,eid,'talk')
 run('dialog','--limit',6)
 run('checkpoint','Genesect316-Panel'+str(eid))
for eid in [135,82]:
 run('eventq',877,eid,'talk')
 run('choose_dialog','Yes|No','Yes','--source',877,eid)
 run('dialog','--limit',12)
run('checkpoint','Genesect316-TitaniaPath')
q=ROOT/'work/316-titania-route.json';q.write_text(json.dumps([[877,0,0,9,41,[]]]))
run('queue_route',q)
run('checkpoint','Genesect316-TitaniaPrepared')
