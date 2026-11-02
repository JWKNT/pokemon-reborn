"""Execute a finite list of root-selected Hardy commands; dry-run default.

Normal current-actor Q inspection, literal HP/stage guards and public HUD only.
No enemy inspection, live saves/logs/AI, adaptive battle policy or replay.
"""
import argparse,json,time,sys,hashlib
from pathlib import Path
from types import SimpleNamespace
import agate_public_action as public
from agate_street_double_queue import actor_context,StepRunner,receipt_guard,step_output
from hypno_turn import canonical,SELF_ITEMS
ROOT=Path(__file__).resolve().parents[1]
SIX={'COFAGRIGUS','SWAMPERT','MIENSHAO','KLINKLANG','EXCADRILL','LUDICOLO'}

class HardyRunner(StepRunner):
    def guarded_command(self):
        epoch,rows=self.snap()
        try:
            guard=public.command_guard(rows,self.args.foes,self.args.mode,captured_at=epoch,now=time.time())
        except ValueError as error:
            if (str(error)!='Independent current Cofagrigus command prompt required'
                and not str(error).startswith('Exact expected visible foe set changed or is unreadable:')):raise
            # The pixel-font Mienshao command is visibly complete but window
            # OCR sometimes drops "do?". Re-OCR the same calibrated game pixels
            # at integer scale, retaining every actor, foe and menu guard.
            crop=self.crop_ocr((0,0,512,384),'command-integer-scale')
            self.report.setdefault('command_crop_proofs',[]).append({'epoch':epoch,'crop':crop})
            rows=crop['rows']
            guard=public.command_guard(rows,self.args.foes,self.args.mode,captured_at=epoch,now=time.time())
        return rows,guard

    def own_hp(self,rows,*,stem):
        if not hasattr(self,'paired_proof'):return super().own_hp(rows,stem=stem)
        proof,epoch=self.paired_proof
        public.need(0<=time.time()-epoch<120,'Paired own inspection expired; no selection')
        self.report[stem+'_paired_own_inspection']={'proof':proof,'epoch':epoch,
            'scope':'This two-selection turn only; no Q after the first action registration'}
        current,guard=self.guarded_command();self.write()
        return proof,current,guard

    def inspect_pair(self,names,actors):
        self.guarded_command();self.keys('q:.12','wait:.4')
        proofs={}
        for i,name in enumerate(actors):
            with actor_context(name,names[name]['totalhp']):
                epoch,rows=self.snap()
                _,labels=public.inspection_context(rows)
                if not any(k=='hp'for k,_,_ in labels):
                    self.keys('down:.12','wait:.25');epoch,rows=self.snap()
                proof=public.inspection_guard(rows)
                proofs[name]=(proof,epoch)
                self.report.setdefault('paired_inspections',[]).append({'actor':name,'epoch':epoch,'rows':rows,'proof':proof});self.write()
            if i==0:self.keys('q:.12','wait:.4')
        self.keys('x:.12','wait:.4');self.guarded_command()
        return proofs

    def run_selection(self):
        rows,guard=self.guarded_command();self.report['initial_rows']=rows;self.report['initial_guard']=guard;self.write()
        hp,rows,re_guard=self.own_hp(rows,stem='before');self.report['initial_hp_proof']=hp;self.write()
        public.need(hp['hp']>=self.args.min_hp,'Actor HP below root-selected threshold; no selection')
        stages=hp.get('explicit_displayed_stages',{})
        for label,minimum in self.args.min_stages.items():
            public.need(label in stages and stages[label]>=minimum,'Required actual own stage missing/below threshold: '+label)
        for label,minimum in self.args.min_effective_stats.items():
            import re
            lines=[x['literal']for x in hp['positioned_own_stat_rows']if x['label']==label]
            public.need(len(lines)==1,'Unique OWN displayed stat required: '+label)
            match=re.search(r':\s*([0-9]{1,4})(?:\s|$)',lines[0])
            public.need(match is not None and int(match[1])>=minimum,'OWN displayed stat missing/below root threshold: '+label)
        rows,guard=self.guarded_command();self.report['pre_action_rows']=rows;self.report['pre_action_guard']=guard;self.write()
        if self.args.item:
            target=self.args.item_target or public.ACTOR
            cmd=[sys.executable,str(ROOT/'scripts/battle_item.py'),self.args.item,target]
            if canonical(self.args.item)in SELF_ITEMS:cmd+=['--active']
        else:cmd=public.helper_argv(self.args,guard)
        self.helper(cmd);self.helper([sys.executable,str(ROOT/'scripts/battle_ready.py')])
        epoch,rows=self.snap();self.report.update(final_rows=rows,final_capture_epoch=epoch,result='selection_returned');self.write()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,required=True);p.add_argument('--roster',type=Path,required=True);p.add_argument('--execute',action='store_true');p.add_argument('--output',type=Path)
    p.add_argument('--paired-inspection',action='store_true',help='Inspect both OWN allies before this exact two-selection turn; Q otherwise cancels first choice')
    a=p.parse_args()
    for path in[a.plan,a.roster]:public.need(path.resolve().is_relative_to(ROOT),'Explicit workspace evidence required')
    plan=json.loads(a.plan.read_text());roster=json.loads(a.roster.read_text());mons=roster['party'];names={m['name']:m for m in mons}
    public.need(len(mons)==6 and len(names)==6 and {m['species']for m in mons}==SIX,'Reviewed actual six required')
    public.need(isinstance(plan,list)and 1<=len(plan)<=12,'Literal finite plan of1..12 selections required')
    for step in plan:
        public.need(set(step)<={'actor','min_hp','min_stages','min_effective_stats','foes','item','item_target','move_slot','target','target_foe'},'Unknown action field')
        public.need(step['actor']in names and type(step['min_hp'])is int and 1<=step['min_hp']<=names[step['actor']]['totalhp'],'Literal owned actor/HP threshold required')
        foes=step['foes'];public.need(len(foes)==2 and len(set(foes))==2 and set(foes)<=public.HARDY,'Two exact public Hardy foes required')
        public.need(('item'in step)^('move_slot'in step),'Choose one action')
        for label,minimum in step.get('min_effective_stats',{}).items():public.need(label in {'attack','defense','spattack','spdefense','speed'}and type(minimum)is int and 1<=minimum<=9999,'Literal named OWN displayed-stat threshold required')
        if 'item'in step:
            public.need(step['item']in{'Ultra Potion','Full Heal','Revive','Revival Herb','X Defend','X Attack','X Accuracy','X Sp. Atk','X Sp. Def','X Speed'},'Unreviewed item')
            public.need(step.get('item_target',step['actor'])in names,'Item target must belong to own six')
            public.need(canonical(step['item'])not in SELF_ITEMS or step.get('item_target',step['actor'])==step['actor'],'X items affect their current actor only')
        else:
            slot=step['move_slot'];public.need(type(slot)is int and 0<=slot<=3,'Literal move slot required')
            public.need(names[step['actor']]['moves'][slot]['move']not in{'EARTHQUAKE','SURF','ROCKSLIDE'},'Ally-damaging spread moves require separate review')
            public.need(step.get('target')in[None,1,3] and (step.get('target')is None or step.get('target_foe')in foes),'Literal physical foe target required')
    bindings={str(q):hashlib.sha256(q.read_bytes()).hexdigest()for q in[a.plan,a.roster]}
    proposal={'dry_run':not a.execute,'bindings':bindings,'selections':plan,'source':public.source_proof(),'policy':'Before each selection: recording health, exact actor/foes/menu, OWN Q HP/stages. Every faint/replacement/refusal or capture restart stops without replay.'};print(json.dumps(proposal,indent=2),flush=True)
    if not a.execute:return 0
    public.need(a.output is not None,'New receipt folder required');folder=a.output.resolve();public.need(folder.is_relative_to(ROOT)and not folder.exists(),'No replay/resume/overwrite');folder.mkdir()
    baseline=json.loads((ROOT/'recordings/capture-health.json').read_text());journal={'kind':'hardy_explicit_double_queue','start_epoch':time.time(),'bindings':bindings,'plan':plan,'completed':[],'pending':None};runner=None
    def write():(folder/'queue.json').write_text(json.dumps(journal,indent=2)+'\n')
    write()
    try:
        paired={}
        if a.paired_inspection:
            public.need(len(plan)==2 and plan[0]['actor']!=plan[1]['actor'],'Exactly one ordered allied pair required')
            source=(public.GAME/'Scripts/Battle_Inspect.rb').read_text()
            public.need('chooseInspectSlot(0, pkmn.index)'in source,'Own-only Q partner cycle source changed')
            pair_path=folder/(folder.name+'-pair-inspection.json')
            args=SimpleNamespace(mode='hardy',foes=plan[0]['foes'],min_hp=1,item=None,move_slot=None,target=None,target_foe=None,output=pair_path,canvas=None)
            with actor_context(plan[0]['actor'],names[plan[0]['actor']]['totalhp']):
                runner=HardyRunner(args,baseline)
                try:paired=runner.inspect_pair(names,[s['actor']for s in plan])
                finally:runner.finish()
            journal['paired_inspection']=pair_path.name;write()
        for i,step in enumerate(plan):
            public.need(time.time()-journal['start_epoch']<600,'Finite queue time limit')
            journal['pending']={'index':i,'selection':step};write();mon=names[step['actor']]
            args=SimpleNamespace(mode='hardy',foes=step['foes'],min_hp=step['min_hp'],min_stages=step.get('min_stages',{}),min_effective_stats=step.get('min_effective_stats',{}),item=step.get('item'),item_target=step.get('item_target'),move_slot=step.get('move_slot'),target=step.get('target'),target_foe=step.get('target_foe'),output=step_output(folder,i),canvas=None)
            with actor_context(step['actor'],mon['totalhp']):
                runner=HardyRunner(args,baseline)
                if paired:runner.paired_proof=paired[step['actor']]
                try:runner.run_selection()
                except BaseException as e:runner.report.update(result='stopped_for_review',error=str(e));raise
                finally:runner.stop_child();runner.finish()
                receipt_guard(runner.report)
            rows=runner.report['final_rows'];prompt=' '.join(r['text']for r in rows if r.get('y',0)>=.72 and r.get('x',1)<.55);actors=[n for n in names if public.name_matches(prompt,n)]
            public.need(len(actors)==1,'Returned actor unreadable/ambiguous; inspect without replay')
            if i+1<len(plan):public.need(actors[0]==plan[i+1]['actor'],'Returned actor differs from next declared selection')
            with actor_context(actors[0],names[actors[0]]['totalhp']):
                runner.guarded_command()
            journal['completed'].append({'index':i,'actor':step['actor'],'receipt':str(args.output),'hp_before':runner.report['initial_hp_proof']});journal['pending']=None;write()
        journal['result']='finite_plan_complete; root reviews next turn'
    except BaseException as e:journal.update(result='stopped_for_review; never replay pending',error=str(e));write();print(journal['result'],str(e),flush=True);return 2
    finally:journal['end_epoch']=time.time();write()
    return 0

if __name__=='__main__':raise SystemExit(main())
