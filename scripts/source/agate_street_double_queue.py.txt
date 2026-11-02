"""Bounded root-selected Lyla/Ezra actions; default dry-run, public UI only.

The root must separately verify the opener and Ditto transformation. This is
an explicit action queue, not an opponent policy or an automatic switcher.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
import agate_public_action as public
from agate_finite_items import public_condition_guard,NO_EFFECT

ROOT=Path(__file__).resolve().parents[1]
FOES={'Noivern','Whimsicott','Wigglytuff','Haxorus','Ditto','Bellossom','Mantine','Kommo-o'}
SPECIES={'COFAGRIGUS','ARCANINE','SWAMPERT','MIENSHAO','EXCADRILL','CRYOGONAL'}
MAX_ACTIONS=16
MAX_SECONDS=600
STOP=re.compile(r'fainted|defeated|for winning|out of usable|about to send|trying to learn|'
                r'change pok|switch your|choose a pok|transformed into|transformed!|'
                r'but it failed|already full|hp is full|there was no target',re.I)
SPREAD={'EARTHQUAKE','SURF','ROCKSLIDE'}


def need(ok,message):
    if not ok:raise ValueError(message)


def step_output(folder,index):
    """Bind the inherited work basename to its queue, not global step-00."""
    folder=Path(folder).resolve()
    need(type(index)is int and 0<=index<MAX_ACTIONS,'Literal finite selection index required')
    queue_id=hashlib.sha256(str(folder).encode()).hexdigest()[:12]
    return folder/f'{folder.name}-{queue_id}-step-{index:02}.json'


@contextmanager
def actor_context(name,total):
    old=public.ACTOR,public.MAX_HP
    public.ACTOR,public.MAX_HP=name,total
    try:yield
    finally:public.ACTOR,public.MAX_HP=old


def validate_plan(plan,roster):
    need(isinstance(plan,list) and 1<=len(plan)<=MAX_ACTIONS,'Choose1..16 explicit selections, at most8double turns')
    mons=roster.get('party',[])
    need(len(mons)==6 and {m.get('species')for m in mons}==SPECIES,'Explicit frozen reviewed six required')
    names={m['name']:m for m in mons};need(len(names)==6,'Unique frozen own names required')
    special=0
    for step in plan:
        need(isinstance(step,dict),'Each selection must be an object')
        need(set(step)<={'actor','min_hp','foes','item','move_slot','target','target_foe','reviewed_spread'},'Unknown action field')
        actor=step.get('actor');need(actor in names,'Actor must belong to the frozen six')
        mon=names[actor];hp=step.get('min_hp')
        need(type(hp)is int and 1<=hp<=mon['totalhp'],'Explicit literal HP threshold required')
        foes=step.get('foes');need(isinstance(foes,list) and len(foes)==2 and len(set(foes))==2 and set(foes)<=FOES,'Two exact declared foes required')
        need(('item'in step)^('move_slot'in step),'Select exactly one item or move')
        if 'item'in step:
            need(step['item'] in {'Ultra Potion','Full Heal','X Sp. Atk'},'Only explicitly reviewed heal/status/singleSpAtk items supported')
            need(not any(k in step for k in ['target','target_foe','reviewed_spread']),'Items target their current actor only')
            if step['item']=='X Sp. Atk':need(not(set(foes)&{'Noivern','Ditto'}),'Handle the opening Noivern/Ditto before further SpAtk setup')
            special+=int(step['item']=='X Sp. Atk')
        else:
            slot=step['move_slot'];need(type(slot)is int and 0<=slot<=3,'Literal move slot0..3 required')
            move=mon['moves'][slot]['move'];need(move!='FAKEOUT','FakeOut turn1 belongs to the separate manual opener')
            if move in SPREAD:need(step.get('reviewed_spread')is True,'Spread damage/partner safety requires explicit root review')
            if 'target'in step:
                need(step['target']in [1,3] and step.get('target_foe')in foes,'Explicit physical foe slot/name required')
            else:need('target_foe'not in step,'Target name requires its physical slot')
    need(special<=1,'At most one explicitly chosen XSpAtk per finite plan')
    return names


def installed_foe_proof():
    source=(public.GAME/'Scripts/Reborn/trainertext.rb').read_text()
    species=set()
    for name,cls in [('Lyla','NWCultistF'),('Ezra','NWCultist')]:
        marker=f':teamid => ["{name}", :{cls}, 1],'
        need(source.count(marker)==1,'Installed street trainer source changed')
        block=source.split(marker,1)[1].split(':teamid',1)[0]
        species.update(re.findall(r':species\s*=>\s*:([A-Z0-9]+)',block))
    expected={'NOIVERN','WHIMSICOTT','WIGGLYTUFF','HAXORUS','DITTO','BELLOSSOM','MANTINE','KOMMOO'}
    need(species==expected and FOES==public.LYLAEZRA,'Declared eight installed opponents changed')
    return {'species':sorted(species),'trainertext_sha256':hashlib.sha256(source.encode()).hexdigest()}


def receipt_guard(report):
    need(report.get('pending')is None and not report.get('journal_issues') and not report.get('final_capture_error'),
         'Partial/ambiguous receipt; stop without replay')
    text=' '.join(t for s in report.get('public_screens',[])for t in s.get('text',[])if isinstance(t,str))
    need(not STOP.search(text),'Faint/replacement/transform/victory boundary; root review required')
    need(not NO_EFFECT.search(text),'Move/item refusal; root review required')
    public_condition_guard(report)


def returned_command_guard(report,foes,names,expected_actor=None):
    rows=report.get('final_rows',[])
    prompt=' '.join(r['text']for r in rows if r.get('y',0)>=.72 and r.get('x',1)<.55)
    actors=[n for n in names if public.name_matches(prompt,n)]
    need(len(actors)==1,'Returned command actor is unreadable/ambiguous; root review required')
    actor=actors[0]
    need(expected_actor is None or actor==expected_actor,'Returned actor differs from next explicit selection')
    with actor_context(actor,names[actor]['totalhp']):
        return public.command_guard(rows,foes,'lylaezra',captured_at=report['final_capture_epoch'],now=time.time())


class StepRunner(public.Runner):
    """Reuse owned Q-inspection and normal helpers; only bounded dispatch differs."""
    def __init__(self,args,baseline):
        self.baseline=baseline;self.child=None
        super().__init__(args)

    def health(self):
        h=super().health()
        need(h.get('pid')==self.baseline.get('pid') and h.get('restart_count',0)==self.baseline.get('restart_count',0),
             'Recorder changed/restarted since queue start; stop without replay')
        need(-2<=time.time()-h.get('epoch',0)<2,'Recorder health is not current')
        return h

    def stop_child(self):
        if self.child is None or self.child.poll()is not None:return
        os.killpg(self.child.pid,signal.SIGTERM)
        try:self.child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(self.child.pid,signal.SIGKILL);self.child.wait(timeout=3)

    def helper(self,cmd):
        before=self.health();stage={'argv':cmd,'start_epoch':time.time()}
        self.report['helpers'].append(stage);self.report['pending']=stage;self.write()
        self.child=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
        try:
            out,err=self.child.communicate(timeout=120)
            stage.update(returncode=self.child.returncode,stdout=out,stderr=err,end_epoch=time.time());self.write()
        except BaseException:
            self.stop_child();stage['stopped_owned_process_group']=True;self.write();raise
        self.stable_capture(before,self.health())
        need(self.child.returncode==0,'Normal helper stopped; inspect public state, no replay')
        self.child=None;self.report['pending']=None;self.write()

    def run_selection(self):
        rows,guard=self.guarded_command();self.report['initial_rows']=rows;self.report['initial_guard']=guard;self.write()
        public_condition_guard({'final_rows':rows})
        hp,rows,re_guard=self.own_hp(rows,stem='before');self.report['initial_hp_proof']=hp;self.write()
        need(hp['hp']>=self.args.min_hp,'Current actor actual HP is below root threshold; no battle action')
        rows,guard=self.guarded_command();self.report['pre_action_rows']=rows;self.report['pre_action_guard']=guard;self.write()
        self.helper(public.helper_argv(self.args,guard))
        self.helper([sys.executable,str(ROOT/'scripts/battle_ready.py')])
        epoch,rows=self.snap();self.report.update(final_rows=rows,final_capture_epoch=epoch,result='selection_returned')
        self.write()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,required=True);p.add_argument('--roster',type=Path,required=True)
    p.add_argument('--execute',action='store_true');p.add_argument('--reviewed-midbattle',action='store_true')
    p.add_argument('--output',type=Path);p.add_argument('--canvas',type=lambda s:tuple(map(int,s.split(','))))
    a=p.parse_args()
    for path in [a.plan,a.roster]:need(path.resolve().is_relative_to(ROOT),'Explicit workspace plan/frozen roster required')
    plan=json.loads(a.plan.read_text());roster=json.loads(a.roster.read_text());names=validate_plan(plan,roster)
    binding={str(x):hashlib.sha256(x.read_bytes()).hexdigest()for x in [a.plan,a.roster]}
    proposal={'dry_run':not a.execute,'source':public.source_proof(),'foe_source':installed_foe_proof(),'bindings':binding,'selections':plan,
              'max_actions':MAX_ACTIONS,'max_seconds':MAX_SECONDS,'no_switches_or_policy':True,
              'gate':'Separate actual opener/transform review; before EVERY selection exact actor/foes/menu/ownedQnumericHP; any boundary stops.'}
    print(json.dumps(proposal,indent=2),flush=True)
    if not a.execute:return 0
    need(a.reviewed_midbattle,'Root must first review opener/transformation and current public state')
    need(a.output is not None,'New output folder required')
    folder=a.output.resolve();need(folder.is_relative_to(ROOT) and not folder.exists(),'New workspace folder only; no resume/replay')
    folder.mkdir();journal={'kind':'agate_street_double_finite_explicit_queue','start_epoch':time.time(),'bindings':binding,'plan':plan,'completed':[],'pending':None}
    def write(): (folder/'queue.json').write_text(json.dumps(journal,indent=2)+'\n')
    baseline=json.loads((ROOT/'recordings/capture-health.json').read_text());write();runner=None
    def cancelled(signum,frame):raise KeyboardInterrupt('Queue cancelled; pending must not be replayed')
    signal.signal(signal.SIGTERM,cancelled);signal.signal(signal.SIGINT,cancelled)
    try:
        for i,step in enumerate(plan):
            need(time.time()-journal['start_epoch']<MAX_SECONDS,'Finite queue time cap reached')
            journal['pending']={'index':i,'step':step};write()
            mon=names[step['actor']]
            args=SimpleNamespace(mode='lylaezra',foes=step['foes'],min_hp=step['min_hp'],item=step.get('item'),
                move_slot=step.get('move_slot'),target=step.get('target'),target_foe=step.get('target_foe'),
                output=step_output(folder,i),canvas=a.canvas)
            with actor_context(step['actor'],mon['totalhp']):
                runner=StepRunner(args,baseline)
                try:runner.run_selection()
                except BaseException as e:runner.report.update(result='stopped_for_review',error=str(e));raise
                finally:runner.stop_child();runner.finish()
                receipt_guard(runner.report)
                returned_command_guard(runner.report,step['foes'],names,
                    plan[i+1]['actor']if i+1<len(plan)else None)
            journal['completed'].append({'index':i,'actor':step['actor'],'receipt':str(args.output),'actual_hp_before':runner.report['initial_hp_proof']['hp']})
            journal['pending']=None;write()
        journal['result']='finite_plan_finished; root must review public state'
    except BaseException as e:
        journal.update(result='stopped_for_review; never replay pending',error=str(e));write();print(journal['result'],str(e),flush=True);return 2
    finally:journal['end_epoch']=time.time();write()
    return 0


if __name__=='__main__':raise SystemExit(main())
