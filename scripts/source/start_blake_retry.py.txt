"""Start the reviewed Blake retry and execute exactly the two opening commands."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
j=json.loads((ROOT/'notes/Blake-defensive-retry-ready-status.json').read_text())
assert j['map']==439 and j['position']==[82,21]
assert [p['name'] for p in j['party'][:2]]==['Cofagrigus','Hexan']
assert all(p['hp']==p['totalhp'] for p in j['party'])
run('trainer_music','start','BLAKE','Blake')
act('up:.12','wait:1');print(read(),flush=True)
run('battle_batch','Cofagrigus',0,'--foes','Gyarados,Mamoswine','--policy',ROOT/'work/Blake-trained-opener.json','--turns',2,'--watch','--status-move')
print('BLAKE OPENING REVIEW',flush=True)
