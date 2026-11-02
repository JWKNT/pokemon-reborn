"""One explicitly reviewed Agate action, normal public UI only; dry-run default.

Only --execute captures screens/uses controls. Warmup numeric HP comes from
normal OWN Q Self Inspect, never foe inspection/internal state. Root chooses
one item or move slot; this wrapper has no setup policy or automatic next turn.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from hypno_turn import (SELF_ITEMS,canonical,deduplicate_screens,name_matches,
                        normalized_name_text,read_generated_screens,run_command_row)

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Applications/Reborn.app/Contents/Game')
ACTOR='Cofagrigus'
MAX_HP=252
CANVASES={(2272,1816):(112,132,2048,1536),(2184,1728):(68,110,2048,1536),(1024,796):(0,28,1024,768)}
WARMUP={'Ludicolo','Beheeyem','Lapras','Magneton','Lanturn','Porygon-Z','Eelektross','Cryogonal','Seismitoad','Clefable'}
RICARDO={'Slurpuff','Minior','Scolipede','Aggron','Blaziken'}
SOLARIS={'Staraptor','Scizor','Gyarados','Tyranitar','Excadrill','Garchomp'}
ANTOINE={'Mamoswine','Lurantis','Liepard','Mightyena','Tyranitar'}
LYLAEZRA={'Noivern','Whimsicott','Wigglytuff','Haxorus','Ditto','Bellossom','Mantine','Kommo-o'}
HARDY={'Gigalith','Aerodactyl','Lycanroc','Archeops','Rampardos'}
MODE_FOES={'warmup':WARMUP,'solaris':SOLARIS,'ricardo':RICARDO,
           'antoine':ANTOINE,'lylaezra':LYLAEZRA,'hardy':HARDY,
           'gym-alistair':{'Lunatone','Carracosta','Armaldo'},
           'gym-xavier':{'Aurorus','Mamoswine'},'gym-noivy':{'Tyranitar','Tyrantrum'}}


def mode_is_double(mode):
    need(mode in MODE_FOES,'Unknown Agate mode')
    return mode in {'warmup','lylaezra','hardy'}


def mode_default_foes(mode):
    need(mode in MODE_FOES,'Unknown Agate mode')
    return {'warmup':['Ludicolo','Beheeyem'],'solaris':['Staraptor'],
            'ricardo':['Slurpuff'],'antoine':['Mamoswine'],
            'lylaezra':['Noivern','Ditto'],'hardy':['Gigalith','Aerodactyl'],
            'gym-alistair':['Lunatone'],'gym-xavier':['Aurorus'],'gym-noivy':['Tyranitar']}[mode]
MESSAGES=re.compile(r'used|critical|fainted|trick.?room|dimensions|twisted|normal|'
                    r'rose|raised|fell|missed|avoided|effective|flinch|burn|sleep|'
                    r'poison|paraly|healed|restored|recovered|wore off|no longer|'
                    r'failed|defeated|for winning|out of usable',re.I)


def need(ok,message):
    if not ok:raise ValueError(message)


def source_proof():
    inspect=GAME/'Scripts/Battle_Inspect.rb';controls=GAME/'Scripts/Controls.rb'
    scene=GAME/'Scripts/Battle_Scene.rb';windows=GAME/'Scripts/SW Subclasses.rb'
    i,c,s,w=[p.read_text() for p in [inspect,controls,scene,windows]]
    need('Q / PgUp:   Previous Page, Self Inspect' in c,'Installed own-inspect key contract changed')
    need('stastr[0] = "HP:                           {1}/{2}"' in i and
         'report.push(_INTL(stastr[0], pkmn.hp, pkmn.totalhp))' in i,
         'Owned doubles exact numeric HP display changed')
    need('(_INTL "Inspecting {1}:", pkmn.name)' in i and
         'elsif Input.trigger?(Input::L)' in s and 'pbShowBattleStats(@battle.battlers[index])' in s,
         'Normal current-actor own inspection changed')
    need('@sprites["cmdwindow"].index = 0' in i and
         'class Window_CommandPokemon_NoPageScroll < Window_CommandPokemon' in i and
         'super(false)' in i and 'if Input.repeat?(Input::DOWN)' in w and
         '@index = (@index + @column_max) % @item_max' in w,
         'Normal bounded own-inspection Down focus contract changed')
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [inspect,controls,scene,windows]}


def hp_pair(text):
    # No substitution of unreadable digits and no bar-to-HP inference.
    pairs={(int(a),int(b)) for a,b in re.findall(r'(?<!\w)([0-9]{1,3})\s*/\s*([0-9]{2,3})(?!\w)',text)}
    need(len(pairs)==1,'One actual numeric current/total HP fraction is required')
    hp,total=next(iter(pairs))
    need(total==MAX_HP and 0<hp<=total,f'Expected living {ACTOR} actual HP/{MAX_HP}')
    return hp,total


def command_guard(rows,foes,mode,*,captured_at,now):
    need(-2<=now-captured_at<=15,'Public command capture is not fresh')
    need(rows and all('text' in r and 'x' in r and 'y' in r for r in rows),'Positioned public OCR rows required')
    body='\n'.join(r['text'] for r in rows).lower()
    need(not re.search(r'de.?feated|for winning|out of usable|choose a pok|switch in|change pok|switch your|fainted',body),
         'Victory/faint/replacement input screen; no action')
    bottom=' '.join(r['text'] for r in rows if r['y']>=.65)
    need(not re.search(r'\bpp\s*[:.]|pp.?\s*\d+\s*/\s*\d+',bottom,re.I),'Move grid already open')
    for label in ['fight','bag']:
        need(any(canonical(r['text'])==label and .53<=r['x']<=.98 and .70<=r['y']<=.88 for r in rows),
             'Fresh standalone Fight/Bag command labels required')
    need(any(run_command_row(r) for r in rows),'Fresh proper Run/RIUN command cell required')
    prompt=' '.join(r['text'] for r in rows if r['y']>=.72 and r['x']<.55)
    plain=normalized_name_text(prompt)
    # Root visually verified the pixel-font "What will" on the fresh Antoine
    # command screen; public OCR consistently rendered exactly "What mill".
    plain=re.sub(r'^what\s+mill\b','what will',plain)
    need(re.search(r'\b[wkh]hat\s+will\b',plain) and name_matches(prompt,ACTOR) and
         re.search(r'\bdo\b',plain),'Independent current Cofagrigus command prompt required')
    after_will=plain.split('will',1)[1].split('do',1)[0]
    need(name_matches(after_will,ACTOR),'Command prompt names another actor')
    actor=[r for r in rows if .37<=r['y']<.70 and r['x']>.5 and name_matches(r['text'],ACTOR)]
    need(actor,'Expected own Cofagrigus HUD')
    need(len(foes)==(2 if mode_is_double(mode) else 1),'Mode requires its exact number of expected foes')
    known=MODE_FOES[mode]
    need(set(foes)<=known and len(set(foes))==len(foes),'Expected foes must be distinct installed mode species')
    enemy=[r for r in rows if r['y']<.37 and r['x']<.5]
    observed={name:[r for r in enemy if name_matches(r['text'],name)] for name in known}
    visible={name for name,hits in observed.items() if hits}
    need(visible==set(foes),'Exact expected visible foe set changed or is unreadable: '+str(sorted(visible)))
    need(all(len(observed[name])==1 for name in foes),'Expected foe HUD names are not unique')
    ordered=sorted(foes,key=lambda n:observed[n][0]['y'])
    return {'actor':ACTOR,'expected_foes':list(foes),'ordered_visible_foes':ordered,
            'actor_hud':actor,'foe_hud':{n:observed[n] for n in foes},'prompt':prompt,
            'capture_epoch':captured_at,'age_seconds':round(now-captured_at,3)}


STAT_LABEL=re.compile(r'^(HP|Attacke|Attack|Defense|Sp[. ]?Attack|Sp[. ]?Defense|Speed|Accuracy|Evasion|Trick Room)(?:\s*[:.!;]\s*|\s*$)',re.I)


def inspection_context(rows):
    need(rows and all('text' in r and 'x' in r and 'y' in r for r in rows),
         'Positioned own-inspection OCR rows required')
    text='\n'.join(r['text'] for r in rows)
    title=' '.join(r['text'] for r in rows if r['y']>.65)
    # Xavier134 own Q title OCR joined two visibly separate words. This
    # literal owned-name alias preserves the independent Inspecting role.
    title=re.sub(r'(?i)(?<!\w)Inspecting(?='+re.escape(ACTOR)+r'\b)','Inspecting ',title)
    need(re.search(r'\binspecting\b',normalized_name_text(title)) and name_matches(title,ACTOR),
         'Only actual Inspecting Cofagrigus own popup is accepted')
    need(not any(n!=ACTOR and name_matches(title,n) for names in MODE_FOES.values() for n in names),
         'Contradictory foe inspection popup')
    labelled=[]
    for row in rows:
        # Session132's own CF popup renders the Attack colon as a final "e".
        # Accept only that exact observed label, after the independent own-title
        # guard; retain original OCR rows/screens as the evidence.
        label_text={'attacke':'Attack:','attackl':'Attack:','httack:':'Attack:'}.get(row['text'].strip().lower(),row['text'].strip())
        m=STAT_LABEL.match(label_text)
        if m and .08<=row['x']<=.95 and 0<=row['y']<.72:
            labelled.append((m.group(1).lower().replace('.','').replace(' ',''),row,m))
    need({'attack','defense'}<=set(key for key,_,_ in labelled),
         'Independent own Attack/Defense inspection rows required')
    anchors={key:[row for k,row,_ in labelled if k==key] for key in ('attack','defense')}
    need(all(len(group)==1 for group in anchors.values()), 'Unique own Attack/Defense anchors required')
    # Both opponent HUDs remain visible behind the OWN inspection popup. Their
    # HP labels must not be counted as ours. Select HP only from the stat column
    # independently proved by Attack and Defense, above both of those rows.
    labelled=[entry for entry in labelled if entry[0]!='hp' or all(
        abs(entry[1]['x']-group[0]['x'])<.15 and entry[1]['y']<group[0]['y']
        for group in anchors.values())]
    return text,labelled


def inspection_guard(rows):
    text,labelled=inspection_context(rows)
    assembled=[]
    for key,row,m in labelled:
        value_rows=[]
        suffix=row['text'].strip()[m.end():].strip()
        if not suffix:
            # OCR often emits the label and right-aligned number separately.
            # Associate only same-line values to the right of that exact label.
            tolerance=min(.025,max(.014,float(row.get('h',.012))*1.2))
            value_rows=[r for r in rows if r is not row and
                        r['x']>row['x']+.035 and abs(r['y']-row['y'])<=tolerance and
                        not STAT_LABEL.match(r['text'].strip())]
            value_rows.sort(key=lambda r:r['x'])
            suffix=' '.join(r['text'].strip() for r in value_rows)
        literal=row['text'].strip()+((' '+suffix) if value_rows else '')
        assembled.append({'label':key,'label_row':row,'value_rows':value_rows,'literal':literal})
    hp_rows=[r for r in assembled if r['label']=='hp']
    need(len(hp_rows)==1,'Exactly one positioned own HP inspection label is required')
    hp_row=hp_rows[0]
    # Reject the ordinary battle HUD HP beneath a different inspection panel.
    for key in ['attack','defense']:
        stat_rows=[r for r in assembled if r['label']==key]
        need(len(stat_rows)==1 and hp_row['label_row']['y']<stat_rows[0]['label_row']['y'] and
             abs(hp_row['label_row']['x']-stat_rows[0]['label_row']['x'])<.15,
             'HP must be above aligned own Attack/Defense inspection rows')
    hp,total=hp_pair(hp_row['literal'])
    # Reborn may display effective stats without explicit stages. Preserve the
    # literal rows; never derive stages from calculated stats or unseen boosts.
    lines=[r['literal'] for r in assembled]
    stages={}
    for line in lines:
        m=re.search(r'^([A-Za-z. ]+):.*?([+-][0-6])\s*$',line)
        if m:stages[m[1].strip()]=int(m[2])
    return {'hp':hp,'total_hp':total,'literal_own_stat_lines':lines,
            'positioned_own_stat_rows':assembled,
            'explicit_displayed_stages':stages,'inspection_text':text}


def helper_argv(args,proof,root=ROOT):
    if args.item:
        cmd=[sys.executable,str(root/'scripts/battle_item.py'),args.item,ACTOR]
        if canonical(args.item) in SELF_ITEMS:cmd+=['--active']
        return cmd
    cmd=[sys.executable,str(root/'scripts/battle_move.py'),str(args.move_slot)]
    if args.target is not None:
        need(mode_is_double(args.mode) and args.target_foe,'A doubles target needs its explicit foe name')
        foe=proof['ordered_visible_foes'][0 if args.target==1 else 1]
        need(foe==args.target_foe,'Actual physical target HUD differs from the reviewed target foe')
        cmd+=[str(args.target)]
    if mode_is_double(args.mode):cmd+=['--foe-names',','.join(proof['ordered_visible_foes'])]
    return cmd+['--watch']


def message_candidates(screens):
    result=[];previous=()
    for i,screen in enumerate(screens):
        lines=tuple(t for t in screen['text'] if MESSAGES.search(t))
        if lines and lines!=previous:result.append({'screen_index':i,'epoch':screen['first_epoch'],'lines':list(lines)})
        previous=lines
    return result


class Runner:
    def __init__(self,args):
        self.args=args;self.path=args.output.resolve();self.txt=self.path.with_suffix('.txt')
        need(self.path.is_relative_to(ROOT) and not self.path.exists() and not self.txt.exists(),
             'NEW workspace output JSON/text required; no replay/overwrite')
        self.work=ROOT/'work'/self.path.stem
        need(not self.work.exists(),'Evidence directory exists; review partial action first')
        self.work.mkdir()
        self.offset=(ROOT/'recordings/screens.jsonl').stat().st_size
        self.report={'kind':'agate_public_one_reviewed_action','start_epoch':time.time(),
                     'mode':args.mode,'expected_actor':ACTOR,'expected_total_hp':MAX_HP,'min_hp':args.min_hp,
                     'expected_foes':args.foes,'explicit_action':{'item':args.item,'move_slot':args.move_slot,
                     'target':args.target,'target_foe':args.target_foe},'source':source_proof(),
                     'helpers':[],'nonturn_ui_actions':[],'pending':None,'result':'not_started',
                     'observation_policy':'public OCR/screens only; no logs/native battle/AI/RNG; omitted text remains unknown',
                     'journal_binding':'appended public screen byte offset + invocation timespan; sole UI controller required'}
        self.write()

    def write(self):self.path.write_text(json.dumps(self.report,indent=2,ensure_ascii=False)+'\n')

    def health(self):
        h=json.loads((ROOT/'recordings/capture-health.json').read_text())
        need(h.get('active') is True and time.time()-h.get('epoch',0)<2,'Recording capture is not fresh; no input')
        return h

    def stable_capture(self,a,b):
        need(a.get('pid')==b.get('pid') and a.get('restart_count',0)==b.get('restart_count',0),
             'Capture restarted; stop and inspect, never repeat pending action')

    def keys(self,*keys):
        from play import act
        before=self.health();self.report['pending']={'nonturn_keys':list(keys),'epoch':time.time()};self.write()
        act(*keys);self.stable_capture(before,self.health())
        self.report['nonturn_ui_actions'].append(self.report['pending']);self.report['pending']=None;self.write()

    def snap(self):
        from play import snap
        self.health();epoch=time.time();rows=snap();return epoch,rows

    def crop_ocr(self,rect,stem):
        from PIL import Image
        from play import NATIVE
        native=Image.open(NATIVE);canvas=self.args.canvas or CANVASES.get(native.size)
        need(canvas and len(canvas)==4,'Calibrated public native canvas required')
        l,t,w,h=canvas
        need(l>=0 and t>=0 and w>0 and h>0 and l+w<=native.width and t+h<=native.height and abs(w/h-4/3)<.01,
             'Public game canvas is invalid')
        x1,y1,x2,y2=rect
        crop=native.crop((round(l+x1*w/512),round(t+y1*h/384),round(l+x2*w/512),round(t+y2*h/384)))
        crop=crop.resize((round((x2-x1)*3),round((y2-y1)*3)),Image.Resampling.NEAREST)
        path=self.work/(stem+'.png');crop.save(path)
        rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe'),str(path)],timeout=20))
        return {'image':str(path),'rows':rows,'text':'\n'.join(r['text'] for r in rows),'canvas':list(canvas)}

    def guarded_command(self):
        epoch,rows=self.snap()
        return rows,command_guard(rows,self.args.foes,self.args.mode,captured_at=epoch,now=time.time())

    def own_hp(self,rows,*,stem):
        if mode_is_double(self.args.mode):
            self.keys('q:.12','wait:.6')
            observations=[]
            for attempt in range(2):
                epoch,inspection=self.snap()
                crop=self.crop_ocr((0,0,512,384),stem+f'-self-inspect-{attempt}')
                # Prove the same OWN popup before even a non-turn Down input.
                observation={'epoch':epoch,'public_rows':inspection,'crop':crop}
                # Full public OCR often retains the fraction slash better than
                # the resized crop. Both use the same strict own-title, stat-
                # column and HP guards; unreadable captions may use the other
                # representation, while contradictory-owner evidence stops.
                try:
                    _,labelled=inspection_context(inspection)
                    preferred_rows=inspection
                    observation['preferred_ocr']='same-frame full public own popup'
                except ValueError as error:
                    if str(error) not in {'Independent own Attack/Defense inspection rows required','Unique own Attack/Defense anchors required'}:raise
                    _,labelled=inspection_context(crop['rows']);preferred_rows=crop['rows']
                    observation['preferred_ocr']='independently guarded own crop'
                observations.append(observation)
                self.report[stem+'_own_inspection_observations']=observations;self.write()
                if not any(key=='hp' for key,_,_ in labelled) and attempt==0:
                    # Source initializes index0. One ordinary Down focuses the
                    # next report row; no Q/W page switching and no blind loop.
                    observation['stop_before_focus']='HP label absent; bounded normal Down focus'
                    self.write();self.keys('down:.12','wait:.25');continue
                try:proof=inspection_guard(preferred_rows)
                except ValueError as error:
                    # In actual132, 3x crop OCR read the slash in237/252 as4,
                    # while the same public full-frame OCR retained237/252.
                    # Use its independently aligned OWN popup; never invent or
                    # repair digits from an ambiguous fraction.
                    if str(error)!='One actual numeric current/total HP fraction is required':raise
                    alternate=crop['rows'] if preferred_rows is inspection else inspection
                    proof=inspection_guard(alternate)
                    proof['fraction_evidence']='same-frame independently guarded full public own popup'
                observation['proof']=proof
                self.report[stem+'_own_inspection']={**observation,'observations':observations};self.write()
                break
            self.keys('x:.12','wait:.6')
            current,command=self.guarded_command()
            self.report[stem+'_returned_command']={'rows':current,'proof':command};self.write()
            return proof,current,command
        own='\n'.join(r['text'] for r in rows if .37<=r['y']<.70 and r['x']>.5)
        try:hp,total=hp_pair(own);evidence={'public_own_hud_text':own}
        except ValueError:
            crop=self.crop_ocr((268,192,512,281),stem+'-own-hud')
            need(name_matches(own,ACTOR) or name_matches(crop['text'],ACTOR),'Fresh guarded own HUD must independently identify Cofagrigus')
            hp,total=hp_pair(crop['text']);evidence={'crop':crop}
        proof={'hp':hp,'total_hp':total,**evidence}
        return proof,rows,None

    def helper(self,cmd):
        before=self.health();stage={'argv':cmd,'start_epoch':time.time()}
        self.report['helpers'].append(stage);self.report['pending']=stage;self.write()
        try:
            p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=180)
            stage.update(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,end_epoch=time.time());self.write()
        except subprocess.TimeoutExpired as e:
            stage.update(returncode=None,stdout=str(e.stdout or ''),stderr=str(e.stderr or ''),end_epoch=time.time());self.write()
            raise RuntimeError('Helper timeout; pending action must not be replayed') from e
        self.stable_capture(before,self.health())
        need(p.returncode==0,'Ordinary helper stopped; inspect actual public screen before another action')
        self.report['pending']=None;self.write()

    def run(self):
        rows,guard=self.guarded_command();self.report['initial_rows']=rows;self.report['initial_guard']=guard;self.write()
        hp,current,re_guard=self.own_hp(rows,stem='before')
        self.report['initial_hp_proof']=hp
        need(hp['hp']>=self.args.min_hp,'Actual HP is below the explicit safe action threshold; no battle action')
        if re_guard:guard=re_guard
        # Fresh same-menu recheck after crop/inspection, before selecting any item/move.
        rows,guard=self.guarded_command();self.report['pre_action_rows']=rows;self.report['pre_action_guard']=guard;self.write()
        self.helper(helper_argv(self.args,guard))
        self.helper([sys.executable,str(ROOT/'scripts/battle_ready.py')])
        self.report['result']='helpers_returned'
        epoch,rows=self.snap();self.report['final_rows']=rows;self.report['final_capture_epoch']=epoch
        body='\n'.join(r['text'] for r in rows).lower()
        if re.search(r'de.?feated|for winning',body):
            self.report['final_classification']='visible_victory_message';return
        try:guard=command_guard(rows,self.args.foes,self.args.mode,captured_at=epoch,now=time.time())
        except ValueError as e:
            self.report['final_classification']='review_required';self.report['final_guard_stop']=str(e);return
        hp,rows,re_guard=self.own_hp(rows,stem='after')
        self.report['final_hp_proof']=hp;self.report['final_rows']=rows
        self.report['final_guard']=re_guard or guard
        self.report['final_classification']='fresh_expected_command'
        self.report['next_action_hp_threshold_met']=hp['hp']>=self.args.min_hp

    def finish(self):
        # Failure cleanup captures public pixels only and sends no further keys.
        if 'final_rows' not in self.report or self.report['result']=='stopped_for_review':
            try:
                epoch,rows=self.snap();self.report['final_rows']=rows;self.report['final_capture_epoch']=epoch
                self.report['final_classification']='review_required'
            except Exception as e:self.report['final_capture_error']=str(e)
        self.report['end_epoch']=time.time()
        screens,issues=read_generated_screens(ROOT/'recordings/screens.jsonl',self.offset,
                                            self.report['start_epoch'],self.report['end_epoch'])
        self.report['public_screens']=deduplicate_screens(screens);self.report['journal_issues']=issues
        self.report['literal_message_candidates']=message_candidates(self.report['public_screens'])
        self.write()
        lines=['Agate explicitly requested ONE public action; no unseen outcome/stage/turn inference.',
               f"Result: {self.report['result']}; final: {self.report.get('final_classification','unavailable')}",
               json.dumps(self.report['explicit_action']),self.report.get('error','')]
        for proof in ['initial_hp_proof','final_hp_proof']:
            if proof in self.report:lines.append(proof+': '+json.dumps(self.report[proof],ensure_ascii=False))
        for group in self.report['literal_message_candidates']:
            lines.append(f"[{group['epoch']:.3f}, screen{group['screen_index']}] "+' | '.join(group['lines']))
        lines+=['FINAL PUBLIC OCR:']+[r['text'] for r in self.report.get('final_rows',[])]
        self.txt.write_text('\n'.join(lines)+'\n')


def main():
    global ACTOR,MAX_HP
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true');p.add_argument('--mode',choices=tuple(MODE_FOES),required=True)
    p.add_argument('--foes',type=lambda s:s.split(','));p.add_argument('--min-hp',type=int,required=True)
    action=p.add_mutually_exclusive_group(required=True);action.add_argument('--item');action.add_argument('--move-slot',type=int,choices=range(4))
    p.add_argument('--target',type=int,choices=(1,3));p.add_argument('--target-foe')
    p.add_argument('--output',type=Path);p.add_argument('--canvas',type=lambda s:tuple(map(int,s.split(','))))
    p.add_argument('--actor',help='Explicit root-selected OWN current actor; public HUD/prompt must independently match')
    p.add_argument('--total-hp',type=int,help='Literal total from the frozen own build; live own fraction must match')
    args=p.parse_args();args.foes=args.foes or mode_default_foes(args.mode)
    need((args.actor is None)==(args.total_hp is None),'Own actor and total HP must be supplied together')
    if args.actor is not None:
        need(args.mode.startswith('gym-') and args.actor in {'Swampert','Ludicolo','Klinklang','Mienshao','Cofagrigus'},'Only the reviewed normal gym trainer actors permit this CLI override')
        need(type(args.total_hp)is int and 1<=args.total_hp<=999,'Literal own total HP required')
        ACTOR,MAX_HP=args.actor,args.total_hp
    need(1<=args.min_hp<=MAX_HP,'Explicit minimum HP must be1..252')
    need(args.item is None or args.item.strip(),'Empty item name')
    known=MODE_FOES[args.mode]
    need(len(args.foes)==(2 if mode_is_double(args.mode) else 1) and len(set(args.foes))==len(args.foes) and
         set(args.foes)<=known,'Explicit expected foe set does not fit the installed mode')
    need(args.target is None or args.move_slot is not None,'Only moves accept an enemy target')
    need(args.target is not None or args.target_foe is None,'Target foe requires target slot')
    if not args.execute:
        print(json.dumps({'status':'source-only; no UI inspected/input sent','source':source_proof(),
                          'actor':ACTOR,'mode':args.mode,'expected_foes':args.foes,'max_hp':MAX_HP,'min_hp':args.min_hp,
                          'action':{'item':args.item,'move_slot':args.move_slot,'target':args.target,'target_foe':args.target_foe},
                          'policy':'one root-selected action; doubles OWN Q inspect numeric HP before/after, X returns; no foe inspection/autoplay'},indent=2));return 0
    need(args.output is not None,'--execute requires a NEW --output journal path')
    runner=Runner(args)
    try:runner.run()
    except Exception as e:runner.report.update(result='stopped_for_review',error=f'{type(e).__name__}: {e}')
    finally:runner.finish()
    print(runner.report['result'],runner.report.get('final_classification','unavailable'),str(runner.path),flush=True)
    return (0 if runner.report['result']=='helpers_returned' and runner.report.get('final_classification') in
            {'fresh_expected_command','visible_victory_message'} else 2)


if __name__=='__main__':raise SystemExit(main())
