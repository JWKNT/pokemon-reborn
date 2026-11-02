"""Toggle a reviewed pillar control through normal UI and save the resulting positions."""
import json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];eid=int(sys.argv[1]);assert eid in [59,60,110,111,112,113,114,115]
session=json.loads((R/'notes/current-run-control.json').read_text())['session']
def run(n,*a):subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,a)],check=True)
run('eventq',840,eid,'talk');run('choose_dialog','Yes|No','Yes','--source',840,eid);run('linear_dialog',840,eid,'--active','--after-last-choice','--past-choice');run('checkpoint',f'Postgame{session}-Toggle{eid}')
