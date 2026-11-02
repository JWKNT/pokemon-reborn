"""Advance Blake's inspected victory scene, accept Cal's ride, and save."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('trainer_music','finish')
run('linear_dialog',439,157,'--active','--past-battle','--until-choice','--log-scripted-bgm')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',439,157,'--active','--past-choice','--past-battle','--log-scripted-bgm')
run('checkpoint','Blake-won-session-end')
j=json.loads((ROOT/'notes/Blake-won-session-end-status.json').read_text())
assert j['trainer']['badges'].count(True)==11,j['trainer']['badges']
assert j['map']==439,j['map']
assert j['route_quests']['193']==30,j['route_quests']
print('BLAKE STOP CHECKPOINT VERIFIED',j['main_quest'],j['position'],flush=True)
