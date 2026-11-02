import os,subprocess,sys
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='10',REBORN_ROUTE_STEP_PAUSE='.12')
for s,a in [('eventq',[846,7,'enter']),('eventq',[841,16,'enter']),('eventq',[846,8,'talk'])]:
 subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
