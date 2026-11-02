"""Verified normal-input Beryl route, with restartable stage boundaries."""
from play import *
from locate import locate
from wtc_push_plan import solve

stage = int(sys.argv[1]) if len(sys.argv) > 1 else 1
def run(script, *args):
    subprocess.run([sys.executable, str(ROOT/'scripts'/(script+'.py')),
                    *map(str, args)], check=True)
def walk(mid, x, y, target=0):
    s=json.loads((ROOT/'notes/navigation-state.json').read_text())
    run('layer_walk',mid,x,y,int(s['switches'].get('410',False)),target)
def pushes(goals, label):
    mid,x,y=locate(476)
    assert mid==476
    s=json.loads((ROOT/'notes/navigation-state.json').read_text())
    p=ROOT/'work'/label
    p.write_text(json.dumps(solve(mid,x,y,s['switches'].get('410',False),goals),indent=2))
    run('wtc_push_queue',p)

if stage <= 1:
    run('wtc_touch',476,64,496,13,24,0,'up')
    walk(496,17,16)
    run('wtc_touch',496,63,476,17,16,0,'up')
    print('BERYL STAGE 1 COMPLETE',flush=True)
if stage <= 2:
    pushes({'16':[8,15],'17':[12,12]},'beryl-upper-live-plan.json')
    print('BERYL STAGE 2 COMPLETE',flush=True)
if stage <= 3:
    run('wtc_touch',476,66,496,15,11,0,'left')
    walk(496,6,14)
    walk(496,4,27)
    run('wtc_exit',496,22)
    print('BERYL STAGE 3 COMPLETE',flush=True)
if stage <= 4:
    walk(475,38,20)
    run('wtc_exit',475,19)
    walk(474,29,32)
    run('wtc_gate',474,39)
    walk(474,43,34)
    run('wtc_exit',474,24)
    run('wtc_gate',488,21)
    run('touch_heal',488,47)
    print('BERYL STAGE 4 COMPLETE; PARTY HEALED',flush=True)
if stage <= 5:
    run('party_lead','Cofagrigus')
    run('wtc_water',488,20,473)
    run('checkpoint','PULSE-Swalot-ready')
    print('PULSE SWALOT PREPARATION COMPLETE',flush=True)
