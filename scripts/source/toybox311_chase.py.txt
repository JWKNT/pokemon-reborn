"""Follow installed Mew disguise scenes through normal UI; verify each quest stage."""
import subprocess,sys,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def run(s,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
def stage(label,expected):
 run('checkpoint',label)
 status=json.loads((R/'notes'/f'{label}-status.json').read_text())
 nav=json.loads((R/'notes'/f'{label}-navigation.json').read_text())
 # Checkpoints contain the game's ordinary, read-only quest-variable snapshot.
 assert int(nav['variables'].get('636',-1))==expected,(label,nav.get('variables',{}).get('636'))
for eid,expected,label in [(77,6,'Mew311-Cubone'),(80,7,'Mew311-Jigglypuff'),(82,8,'Mew311-Chikorita'),(84,9,'Mew311-Portal')]:
 run('eventq',874,eid,'talk')
 run('linear_dialog',874,eid,'--source-page',0,'--burst','--world-settle','9')
 stage(label,expected)
run('eventq',874,4,'enter')
run('linear_dialog',875,12,'--source-page',0,'--world-settle','9')
stage('Mew311-Forest',10)
print('FOREST ENTRY COMPLETE; review route to southern exit',flush=True)
