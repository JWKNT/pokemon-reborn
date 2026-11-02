"""Win a reviewed Bouffalant encounter and accept its Tauros riding reward."""
from play import *
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
encounter_epoch=time.time()
t=read().lower();assert 'bouffalant' in re.sub(r'\s+','',t) and 'attacked' in re.sub(r'\s+','',t)
act('c','wait:4');run('battle_ready');run('battle_batch','Zapdos',1,'--foes','Bouffalant','--wild','--turns',6)
for _ in range(12):
 t=read().lower();print(t,flush=True)
 if re.search(r'\b(?:yes|tes)\b',t) and 'ride' in t and 'tauros' in t:break
 if 'tauros' in t and any(z in t for z in ['roars','thankful']):act('c','wait:.8')
 else:raise SystemExit('Mount reward review')
else:raise SystemExit('No riding prompt')
act('c','wait:3')
t=read().lower()
if 'dismount' in t:act('c','wait:1')
run('forest_tail245');run('close_wild_music','Bouffalant','--since',encounter_epoch);run('checkpoint',sys.argv[1])
