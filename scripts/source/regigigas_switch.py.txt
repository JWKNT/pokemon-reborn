"""Press one installed, reviewed Regigigas puzzle switch using normal UI, then save."""
import json, pathlib, subprocess, sys
R=pathlib.Path(__file__).resolve().parents[1]
eid=int(sys.argv[1]);stages={44:2,47:5,48:6,52:7,53:8,54:9,55:10,73:11,74:12,78:13,91:15,92:16,93:17,94:18}
assert eid in stages
source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'840','0','0'],stderr=subprocess.DEVNULL))
cs=source['events'][str(eid)]['list'];assert any(c['code']==122 and c['parameters']==[588,588,0,0,stages[eid]] for c in cs)
assert not any('pbTrainerBattle' in str(c) or 'pbWildBattle' in str(c) for c in cs)
def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True)
run('eventq',840,eid,'talk')
run('choose_dialog','Yes|No','Yes','--source',840,eid)
run('linear_dialog',840,eid,'--active','--after-last-choice','--past-choice')
session=json.loads((R/'notes/current-run-control.json').read_text())['session']
run('checkpoint',f'Postgame{session}-RegigigasSwitch{eid}')
v=json.loads((R/'notes/navigation-state.json').read_text());assert v['variables']['588']==stages[eid]
print('PUZZLE SWITCH VERIFIED',eid,stages[eid])
