"""Inspect two owned active allies with Q, then return to the first command.

No battle action, enemy inspection, save/log/internal battle read, or policy.
"""
import argparse,json,time
from pathlib import Path
from types import SimpleNamespace
import agate_public_action as public
from agate_street_double_queue import actor_context
from hardy_double_queue import HardyRunner

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--roster',type=Path,required=True)
    p.add_argument('--actors',required=True)
    p.add_argument('--foes',required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();names={m['name']:m for m in json.loads(a.roster.read_text())['party']}
    actors=a.actors.split(',');foes=a.foes.split(',')
    public.need(len(actors)==2 and len(set(actors))==2 and set(actors)<=names.keys(),'Two literal owned names required')
    baseline=json.loads((public.ROOT/'recordings/capture-health.json').read_text())
    args=SimpleNamespace(mode='hardy',foes=foes,min_hp=1,item=None,move_slot=None,target=None,target_foe=None,output=a.output,canvas=None)
    with actor_context(actors[0],names[actors[0]]['totalhp']):
        r=HardyRunner(args,baseline)
        try:
            proofs=r.inspect_pair(names,actors)
            print(json.dumps({name:{'epoch':ep,'hp':proof['hp'],'stats':proof['literal_own_stat_lines']}for name,(proof,ep)in proofs.items()},indent=2))
            r.report['result']='own_pair_inspected_no_battle_selection';r.write()
        finally:r.finish()
if __name__=='__main__':main()
