import os,subprocess,sys
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='56')
for s,a in [('overworld',[]),('fly_to',['564','--carrier','Rayquaza']),('pavilion375_focus_pickup',[])]:
 subprocess.run([sys.executable,'scripts/'+s+'.py',*a],check=True)
