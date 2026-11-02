import os,subprocess,sys
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56',REBORN_ROUTE_STEP_PAUSE='.12')
for s,*a in [('party_front','Latias'),('eventq',889,54,'talk'),('checkpoint','Picnic385-Healed')]:
 print('PREPARE385',s,*a,flush=True)
 subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
