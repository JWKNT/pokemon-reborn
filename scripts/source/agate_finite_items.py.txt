"""Finite root-selected Agate item queue; default dry-run, public UI only.

Each item delegates to the independently guarded agate_public_action wrapper.
One automatic Ultra Potion is allowed only after its exact no-action low-HP
stop. There is no battle policy, inferred boost tracking or pending replay.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
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

from agate_public_action import (ACTOR,GAME,MAX_HP,MODE_FOES,ROOT,
                                command_guard,helper_argv,mode_is_double,need,source_proof)
from hypno_turn import name_matches,normalized_name_text

MAX_ITEMS=8
MAX_INVOCATIONS=16
MAX_SECONDS=900
LOW_HP_ERROR='ValueError: Actual HP is below the explicit safe action threshold; no battle action'
NO_EFFECT=re.compile(r"won.?t (?:go|rise) any higher|cannot (?:be used|rise)|can't be used|"
                     r"(?:had|has|have) no effect|won.?t have any effect|stat.+maximum",re.I)
STATUS_CHANGE=re.compile(r'\b(?:fell\s+asleep|(?:was|is|became)\s+(?:badly\s+)?(?:poisoned|burned|'
                         r'paraly[sz]ed|frozen(?:\s+solid)?|confused|drowsy)|became\s+confused|'
                         r'status\s*[:.]\s*(?:sleep|asleep|poison(?:ed)?|burn(?:ed)?|frozen|paraly[sz]ed))\b',re.I)
CONDITIONS_CHANGE=re.compile(r'\b(?:used\s+(?:trick\s*room|rain\s*dance|sunny\s*day|hail|sandstorm|'
                            r'(?:electric|grassy|misty|psychic)\s*terrain)|'
                            r'(?:twisted(?:\s+the)?\s+dimensions|dimensions\s+(?:were\s+)?twisted)|'
                            r'(?:field|terrain|weather)\s+(?:has\s+|was\s+|is\s+)?(?:changed|transformed|'
                            r'became|returned|reverted|disappeared|destroyed|inverted|flattened)|'
                            r'started\s+to\s+(?:rain|hail)|(?:rain|hail)\s+(?:started|stopped)|'
                            r'sunlight\s+(?:turned\s+harsh|faded)|sandstorm\s+(?:brewed|kicked\s+up|subsided)|'
                            r'strong\s+winds\s+kicked\s+up)\b',re.I)
OWN_STAT_DROP=re.compile(
    r"(?P<owner>[^\W\d_]+)\s*['’]\s*s\s+"
    r"(?P<stat>(?:sp\.?\s*|special\s+)?(?:defen[cs]e|def\.?|attack|atk\.?)|accuracy|speed)"
    r"\s+(?:(?:sharply|harshly|severely|greatly|drastically|dramatically)\s+)?"
    r"(?:fell|(?:was\s+)?(?:lowered|decreased|dropped|reduced))\b",re.I)
SWAGGER_USE=re.compile(r'\bused\s+swagger\b',re.I)


def words(text):return re.sub(r'[^a-z0-9]+',' ',text.lower()).strip()


def message_scopes(lines):
    """Permit bounded OCR line wraps without mixing messages across screens."""
    return [' '.join(lines[i:i+span]) for i in range(len(lines))
            for span in range(1,min(3,len(lines)-i)+1)]


def negative_own_stat_message(text):
    """Require possessive own-name attribution, never a nearby HUD name.

    Exact message grammar prevents joining an own boost to a later foe drop.
    Existing one-substitution name matching covers observed Cofagrigue OCR.
    No unseen stages or effective numeric stats are inferred from this text.
    """
    normalized=normalized_name_text(text)
    for match in OWN_STAT_DROP.finditer(normalized):
        if name_matches(match['owner'],ACTOR):
            prefix=normalized[:match.start()]
            if re.search(r'\b(?:opposing|foe|enemy)\s*$',prefix):continue
            return match.group(0)
    return None


@lru_cache(maxsize=1)
def installed_field_change_messages():
    # Parse literal static Ruby hash keys only; never evaluate game source.
    found=[];inside=False
    for line in (GAME/'Scripts/Reborn/fieldtext.rb').read_text().splitlines():
        if ':changeMessage' in line and '=>' in line:
            tail=line.split('{',1)[1]
            inside=not tail.lstrip().startswith('}')
            continue
        if not inside:continue
        if re.match(r'\s*\}',line):inside=False;continue
        m=re.match(r'\s*"((?:[^"\\]|\\.)*)"\s*=>',line)
        if m and '{' not in m.group(1) and '#' not in m.group(1):
            phrase=m.group(1).replace('\\"','"')
            if len(words(phrase))>=12:found.append(phrase)
    need(found,'Installed field-change message contract unavailable')
    return tuple(sorted(set(found)))


def public_condition_guard(report):
    rows=report.get('final_rows',[])
    for row in rows:
        if .37<=row.get('y',-1)<.70 and row.get('x',0)>.5:
            need(not (set(words(row.get('text','')).split()) & {'slp','frz','psn','par','brn','tox'}),
                 'Visible own status requires manual threshold review before another item')
    groups=[[r.get('text','') for r in rows]]
    groups.extend([t for t in s.get('text',[]) if isinstance(t,str)]
                  for s in report.get('public_screens',[]))
    groups.extend([t for t in g.get('lines',[]) if isinstance(t,str)]
                  for g in report.get('literal_message_candidates',[]))
    texts=[t for group in groups for t in group]
    for group in groups:
        for scope in message_scopes(group):
            drop=negative_own_stat_message(scope)
            need(drop is None,'Public own stat drop requires fresh OWN Q stats and threshold review: '+
                 (drop or ''))
            need(not SWAGGER_USE.search(normalized_name_text(scope)),
                 'Public Swagger use changes own Attack/confusion risk; manual Foul Play/threshold review required')
    body=' '.join(texts)
    need(not re.search(r'\bsolar(?:is|ts)\s+used\s+(?:the\s+|a\s+)?full\s*restore\b',body,re.I), 'Solaris FullRestore may clear the reviewed burn; root must recheck before another queued item')
    match=STATUS_CHANGE.search(body) or CONDITIONS_CHANGE.search(body)
    need(match is None,'Public status/field/weather/Trick Room change requires manual threshold review: '+
         (match.group(0) if match else ''))
    normalized=' '+words(body)+' '
    for phrase in installed_field_change_messages():
        need(' '+words(phrase)+' ' not in normalized,
             'Installed field-change message requires manual threshold review: '+phrase)
    # Continuing known hail/rain/sandstorm chip is not a transition; actual HP
    # remains independently guarded by the child and each requested threshold.


def validate_plan(plan):
    need(isinstance(plan,list) and 1<=len(plan)<=MAX_ITEMS,'Sequence must contain1..8 explicit items')
    result=[]
    for step in plan:
        need(isinstance(step,dict) and set(step)=={'item','min_hp'},'Each step must have exactly item and min_hp')
        item=step['item'];hp=step['min_hp']
        need(isinstance(item,str) and item.strip()==item and 0<len(item)<=80 and
             not any(ord(c)<32 for c in item),'Each item needs a nonempty literal name')
        need(type(hp) is int and 1<=hp<=MAX_HP,'Each literal min_hp must be1..252')
        result.append({'item':item,'min_hp':hp})
    return result


def validate_foes(mode,foes):
    need(mode in MODE_FOES,'Unknown Agate mode')
    known=MODE_FOES[mode]
    need(isinstance(foes,list) and all(isinstance(n,str) for n in foes) and
         len(foes)==(2 if mode_is_double(mode) else 1) and len(set(foes))==len(foes) and
         set(foes)<=known,'Distinct exact installed foes required for this mode')
    return list(foes)


def validate_output(path,root=ROOT):
    path=path.expanduser().resolve()
    need(path.is_relative_to(root.resolve()) and not path.exists(),
         'A NEW workspace output directory is required; no resume/replay/overwrite')
    need(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}',path.name) is not None,
         'Output directory name must be1..80 simple letters/digits/._-')
    return path


def numeric_hp(proof):
    need(isinstance(proof,dict) and type(proof.get('hp')) is int and
         type(proof.get('total_hp')) is int and proof['total_hp']==MAX_HP and
         0<proof['hp']<=MAX_HP,'Actual positive literal HP/252 proof required')
    return proof['hp']


def classify_child(report,*,mode,foes,step,returncode,now):
    """Validate only this invocation's own child journal, never historic logs."""
    need(isinstance(report,dict) and report.get('kind')=='agate_public_one_reviewed_action',
         'Expected guarded public child journal')
    need(report.get('mode')==mode and report.get('expected_actor')==ACTOR and
         report.get('expected_total_hp')==MAX_HP and report.get('min_hp')==step['min_hp'] and
         report.get('expected_foes')==foes,'Child request binding changed')
    need(report.get('explicit_action')=={'item':step['item'],'move_slot':None,
                                       'target':None,'target_foe':None},'Child action binding changed')
    need(report.get('pending') is None and not report.get('journal_issues') and
         not report.get('final_capture_error'),'Pending or ambiguous child receipt; never replay')
    rows=report.get('final_rows',[])
    captured=report.get('final_guard',{}).get('capture_epoch',report.get('final_capture_epoch'))
    need(type(captured) in (int,float),'Child final public capture time is absent')
    command_guard(rows,foes,mode,captured_at=captured,now=now)
    public_condition_guard(report)
    initial_hp=numeric_hp(report.get('initial_hp_proof'))
    if report.get('error')==LOW_HP_ERROR:
        need(returncode==2 and report.get('result')=='stopped_for_review' and
             report.get('helpers')==[] and 'pre_action_guard' not in report and
             initial_hp<step['min_hp'],
             'Low-HP exception is not proven to have sent no battle action')
        return {'outcome':'low_hp_no_action','initial_hp':initial_hp}
    need(returncode==0 and report.get('result')=='helpers_returned' and
         report.get('final_classification')=='fresh_expected_command' and
         not report.get('error'),'Child action did not return to the exact expected command; stop')
    need(initial_hp>=step['min_hp'],'Action receipt initial HP failed its requested threshold')
    helpers=report.get('helpers')
    args=SimpleNamespace(item=step['item'],mode=mode,move_slot=None,target=None,target_foe=None)
    expected=[helper_argv(args,{}),[sys.executable,str(ROOT/'scripts/battle_ready.py')]]
    need(isinstance(helpers,list) and len(helpers)==2 and
         all(h.get('argv')==argv and h.get('returncode')==0 for h,argv in zip(helpers,expected)),
         'Exact item+ready helper receipts required; no partial or extra dispatch')
    final_hp=numeric_hp(report.get('final_hp_proof'))
    text='\n'.join(t for s in report.get('public_screens',[]) for t in s.get('text',[]) if isinstance(t,str))
    need(not NO_EFFECT.search(text),'Public item refusal/no-effect message; stop without replay')
    return {'outcome':'fresh_expected_command','initial_hp':initial_hp,'final_hp':final_hp,
            'proof_scope':'Selected item helper returned to the guarded command; no unseen consumption/stages inferred'}


def pilot_receipt(report,*,mode,foes,now):
    need(isinstance(report,dict) and type(report.get('end_epoch')) in (int,float) and
         0<=now-report['end_epoch']<=MAX_SECONDS,
         'A completed same-mode public pilot from the last15minutes is required')
    action=report.get('explicit_action',{})
    step={'item':action.get('item'),'min_hp':report.get('min_hp')}
    validate_plan([step])
    pilot_foes=validate_foes(mode,report.get('expected_foes'))
    need(set(pilot_foes)==set(foes),'Pilot exact foe set changed')
    proof=classify_child(report,mode=mode,foes=pilot_foes,step=step,returncode=0,
                         now=report['end_epoch'])
    need(proof['outcome']=='fresh_expected_command','Pilot was not a completed reviewed action')
    return {'pilot_end_epoch':report['end_epoch'],'age_seconds':round(now-report['end_epoch'],3),
            'mode':mode,'foes':foes,'item':step['item'],
            'scope':'Completed public pilot proves wrapper operation only; its HP/stats are never current-action evidence'}


def run_plan(plan,invoke,progress=lambda report:None):
    """Pure finite sequencing; invoke is the sole explicit execution boundary."""
    plan=validate_plan(plan)
    report={'result':'running','planned_items':plan,'invocations':0,'completed_items':0,
            'steps':[],'automatic_heal_wrapper_invocations':0,'max_invocations':MAX_INVOCATIONS}
    progress(report)

    def call(step,index,role):
        need(report['invocations']<MAX_INVOCATIONS,'16-invocation cap reached; no more inputs')
        report['invocations']+=1
        if role=='one-heal':report['automatic_heal_wrapper_invocations']+=1
        progress(report)
        result=invoke(step,index,role,report['invocations'])
        need(result.get('outcome') in {'fresh_expected_command','low_hp_no_action'},
             'Unknown child result; stop without replay')
        return result

    try:
        for index,step in enumerate(plan):
            record={'index':index,'requested':step,'receipts':[],'heal_requested':False}
            report['steps'].append(record);progress(report)
            outcome=call(step,index,'item');record['receipts'].append(outcome);progress(report)
            if outcome['outcome']=='low_hp_no_action':
                record['heal_requested']=True;progress(report)
                heal=call({'item':'Ultra Potion','min_hp':1},index,'one-heal')
                record['receipts'].append(heal);progress(report)
                need(heal['outcome']=='fresh_expected_command','Single heal was not unambiguously completed; stop')
                need(type(heal.get('final_hp')) is int and heal['final_hp']>=step['min_hp'],
                     'HP is still below the requested threshold after one heal; stop without a heal loop')
                outcome=call(step,index,'retry-once');record['receipts'].append(outcome);progress(report)
                need(outcome['outcome']=='fresh_expected_command',
                     'Retried item stopped; no second heal/retry is permitted')
            record['result']='reviewed_item_helper_returned';report['completed_items']+=1;progress(report)
        report['result']='complete'
    except Exception as e:
        report.update(result='stopped_for_review',error=f'{type(e).__name__}: {e}')
    progress(report)
    return report


class Runner:
    def __init__(self,args,plan):
        self.args=args;self.plan=plan;self.path=validate_output(args.output_dir)
        self.start=time.time();self.baseline=self.health()
        wrapper=ROOT/'scripts/agate_public_action.py'
        need(LOW_HP_ERROR.removeprefix('ValueError: ') in wrapper.read_text(),
             'Installed wrapper exact no-action low-HP contract changed')
        self.base={'kind':'agate_finite_root_selected_items','start_epoch':self.start,
                   'mode':args.mode,'expected_foes':args.foes,'actor':ACTOR,
                   'capture_baseline':self.baseline,'source':source_proof(),
                   'field_transition_source_sha256':hashlib.sha256((GAME/'Scripts/Reborn/fieldtext.rb').read_bytes()).hexdigest(),
                   'reviewed_pilot':args.pilot_proof,
                   'wrapper_sha256':hashlib.sha256(wrapper.read_bytes()).hexdigest(),
                   'pending':None,'children':[],'policy':'max8 explicit items; max16 total wrapper invocations; one heal per low-HP no-action step; no boosts/AI/RNG/native/log inference'}
        self.path.mkdir(parents=True);self.save({'result':'not_started'})

    def health(self):
        h=json.loads((ROOT/'recordings/capture-health.json').read_text())
        need(h.get('active') is True and time.time()-h.get('epoch',0)<2,
             'Recording capture is not fresh; no input')
        if hasattr(self,'baseline'):
            need(h.get('pid')==self.baseline.get('pid') and
                 h.get('restart_count',0)==self.baseline.get('restart_count',0),
                 'Capture restarted during finite queue; stop without replay')
        return h

    def save(self,sequence):
        self.sequence=json.loads(json.dumps(sequence))
        (self.path/'queue.json').write_text(json.dumps({**self.base,'sequence':self.sequence},indent=2,ensure_ascii=False)+'\n')

    def stop_owned_child(self,p):
        # start_new_session gives this wrapper/descendants their own group.
        try:os.killpg(p.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        try:return p.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            return p.communicate()

    def invoke(self,step,index,role,number):
        self.health();remaining=MAX_SECONDS-(time.time()-self.start)
        need(remaining>0,'15-minute finite queue limit reached; no more inputs')
        child_path=self.path/f'{self.path.name}-{number:02d}-{role}.json'
        # The child also places evidence under work/<journal-stem>.
        need(not child_path.exists() and not (ROOT/'work'/child_path.stem).exists(),
             'Child journal/evidence already exists; no replay')
        cmd=[sys.executable,str(ROOT/'scripts/agate_public_action.py'),'--execute',
             '--mode',self.args.mode,'--foes',','.join(self.args.foes),'--item',step['item'],
             '--min-hp',str(step['min_hp']),'--output',str(child_path)]
        if self.args.canvas:cmd+=['--canvas',self.args.canvas]
        record={'number':number,'plan_index':index,'role':role,'step':step,'argv':cmd,
                'journal':str(child_path),'start_epoch':time.time()}
        self.base['children'].append(record);self.base['pending']=record;self.save(self.sequence)
        try:
            p=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               text=True,start_new_session=True)
            stdout,stderr=p.communicate(timeout=min(420,remaining))
            record.update(returncode=p.returncode,stdout=stdout,stderr=stderr,end_epoch=time.time())
        except subprocess.TimeoutExpired as e:
            # The group is exclusively this spawned wrapper and its helpers.
            # Stop descendants too; never leave a timed-out input worker alive.
            stdout,stderr=self.stop_owned_child(p)
            record.update(returncode=p.returncode,stdout=stdout,stderr=stderr,
                          timeout=True,end_epoch=time.time())
            self.save(self.sequence);raise RuntimeError('Child timed out; pending must never be replayed') from e
        except BaseException as e:
            if 'p' in locals():
                stdout,stderr=self.stop_owned_child(p)
                record.update(returncode=p.returncode,stdout=stdout,stderr=stderr)
            record.update(interrupted=True,error=f'{type(e).__name__}: {e}',end_epoch=time.time())
            self.save(self.sequence);raise
        self.save(self.sequence);self.health()
        need(child_path.is_file(),'Child journal absent; pending action is ambiguous')
        raw=child_path.read_bytes();child=json.loads(raw)
        outcome=classify_child(child,mode=self.args.mode,foes=self.args.foes,step=step,
                               returncode=p.returncode,now=time.time())
        record.update(journal_sha256=hashlib.sha256(raw).hexdigest(),classification=outcome,
                      literal_message_candidates=child.get('literal_message_candidates',[]))
        self.base['pending']=None;self.save(self.sequence)
        return {**outcome,'journal':str(child_path),'journal_sha256':record['journal_sha256']}

    def run(self):
        def interrupted(number,frame):
            raise InterruptedError(f'Signal{number}: stop owned child and preserve pending; never replay')
        previous={s:signal.signal(s,interrupted) for s in (signal.SIGINT,signal.SIGTERM)}
        try:result=run_plan(self.plan,self.invoke,self.save)
        finally:
            for number,handler in previous.items():signal.signal(number,handler)
        self.base['end_epoch']=time.time();self.save(result)
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true')
    p.add_argument('--mode',choices=tuple(MODE_FOES),required=True)
    p.add_argument('--foes',required=True,type=lambda s:s.split(','))
    p.add_argument('--sequence',required=True,type=Path,help='JSON array of exact item/min_hp objects')
    p.add_argument('--output-dir',type=Path)
    p.add_argument('--pilot-journal',type=Path,help='Completed same-mode/exact-foe public one-action receipt from last15min')
    p.add_argument('--canvas',help='Optional root-calibrated canvas passed to public child wrapper')
    args=p.parse_args();args.foes=validate_foes(args.mode,args.foes)
    plan=validate_plan(json.loads(args.sequence.read_text()))
    if args.output_dir:validate_output(args.output_dir)
    if not args.execute:
        print(json.dumps({'status':'dry-run; no UI/input/output created','mode':args.mode,
                          'foes':args.foes,'sequence':plan,'max_items':MAX_ITEMS,
                          'max_total_wrapper_invocations':MAX_INVOCATIONS,'source':source_proof(),
                          'installed_field_change_message_count':len(installed_field_change_messages()),
                          'low_hp_exception':LOW_HP_ERROR,'pilot_required_for_execute':True,
                          'auto_heal':'one Ultra Potion min_hp1 onlyafterprovennoaction; actualposthealHPmustmeetrequestedthreshold; thenoneNEWretryjournal'},indent=2));return 0
    need(args.output_dir is not None,'--execute requires a NEW --output-dir')
    need(args.pilot_journal is not None,'--execute requires a reviewed completed --pilot-journal')
    pilot=args.pilot_journal.resolve()
    need(pilot.is_relative_to(ROOT) and pilot.is_file(),'Completed pilot must be a workspace public journal')
    raw=pilot.read_bytes()
    args.pilot_proof={**pilot_receipt(json.loads(raw),mode=args.mode,foes=args.foes,now=time.time()),
                      'journal':str(pilot),'sha256':hashlib.sha256(raw).hexdigest()}
    runner=Runner(args,plan);result=runner.run()
    print(result['result'],str(runner.path/'queue.json'),flush=True)
    return 0 if result['result']=='complete' else 2


if __name__=='__main__':raise SystemExit(main())
