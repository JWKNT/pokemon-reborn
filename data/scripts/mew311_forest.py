"""Reviewed forest chase via normal controls, with fresh ordinary checkpoint gates."""
import subprocess,sys,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def run(s,*a,check=True):return subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=check)
def stage(label,want):
 run('checkpoint',label)
 n=json.loads((R/'notes'/f'{label}-navigation.json').read_text())
 assert n['variables']['636']==want,(label,n['variables']['636'])
run('q','875,69,41',check=False)
run('linear_dialog',875,13,'--source-page',1,'--burst','--world-settle',12)
stage('Mew311-ForestExit',12)
run('eventq',875,9,'enter')
run('q','840,152,111',check=False)
run('linear_dialog',840,157,'--source-page',0,'--burst','--world-settle',9)
stage('Mew311-Rhodochrine',13)
run('q','840,137,69',check=False)
run('linear_dialog',840,162,'--source-page',1,'--burst','--world-settle',12)
stage('Mew311-FernCaged',17)
run('eventq',840,13,'talk')
run('checkpoint','Mew311-FernFreed')
n=json.loads((R/'notes/Mew311-FernFreed-navigation.json').read_text());assert not n['switches']['1384']
run('eventq',840,14,'talk')
run('linear_dialog',840,14,'--source-page',1,'--until-choice')
print('FERN FAST TRAVEL YES/NO READY; answer Yes after public review',flush=True)
