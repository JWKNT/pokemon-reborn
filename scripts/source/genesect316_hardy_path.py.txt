from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
def panel(eid):
 run('eventq',877,eid,'talk');run('dialog','--limit',6);run('checkpoint','Genesect316-Panel'+str(eid))
def toggle(eid):
 run('eventq',877,eid,'talk');run('choose_dialog','Yes|No','Yes','--source',877,eid);run('dialog','--limit',12)
for eid in [103,108]:panel(eid)
toggle(82);run('checkpoint','Genesect316-Path10')
panel(98)
for eid in [82,135]:toggle(eid)
run('checkpoint','Genesect316-Path11')
toggle(164);run('checkpoint','Genesect316-Combustion')
q=ROOT/'work/316-hardy-route.json';q.write_text(json.dumps([[877,0,0,71,44,[]]]));run('queue_route',q)
run('checkpoint','Genesect316-HardyPrepared')
