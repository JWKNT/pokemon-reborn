"""A reviewed Perish Song lead, followed by a faster Recover user to stall.

Caller must review both speed matchups and incoming damage. Stops on unknown foes,
party-selection ambiguity, loss, or a new opponent; no party/save data edits.
"""
from play import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--foes',required=True);p.add_argument('--singer',default='Kricketune');p.add_argument('--wall',default='Hexan');p.add_argument('--recover-slot',type=int,default=2);p.add_argument('--resume-song',action='store_true');a=p.parse_args()
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(script+'.py')),*map(str,args)],check=True)
if a.resume_song:run('battle_ready')
else:run('battle_switch',a.singer)
run('battle_batch',a.singer,3,'--foes',a.foes,'--turns',1,'--watch','--status-move')
t=read().lower()
if 'choose a pok' in t or ('cancel' in t and t.count('hp')>=5):run('party_pick',a.wall)
elif 'fight' in t:run('battle_switch',a.wall)
else:raise SystemExit('Perish relay phase review')
run('battle_batch',a.wall,a.recover_slot,'--foes',a.foes,'--turns',3,'--watch','--status-move','--stop-after-battle')
