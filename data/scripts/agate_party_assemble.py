"""Bounded normal Agate PC assembly; source-only dry-run unless --execute.

Development/import never observes or controls the game. Execution starts from
an explicit frozen Circus checkpoint after Cofa preparation/shopping, uses
ordinary Circus PC/party menus, and saves only the final Circus party proof.
Existing journals are never replayed; review a partial stop manually.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from calcenon_agate_queue import Runner as Base, event, need, selected_page
from agate_archive_core import full_pp
from text_speed_max import CANVASES, alignment, find_arrow, norm, pause_guard, unique_label

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Applications/Reborn.app/Contents/Game')
START=('COFAGRIGUS','TRANQUILL','SWAMPERT','MIENSHAO','ARCANINE','EXCADRILL')
FINAL=('COFAGRIGUS','ARCANINE','SWAMPERT','MIENSHAO','EXCADRILL','CRYOGONAL')
CF_EV=[172,4,252,80,0,2]
CF_MOVES=['TRICKROOM','HEX','WILLOWISP','DARKPULSE']
COMMIT_EVENTS=(110,113,114,115,116,117)
TRAINERS=(45,46,48,49,133,134)
IDENTITY=('species','form','name','level','item','ability','nature','natureflag','ev','iv',
          'totalhp','attack','defense','spatk','spdef','speed')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def effective_nature(mon):
    return mon.get('natureflag') or mon['nature']


def source_proof():
    proof=[]
    dimensions=json.loads(subprocess.check_output(['ruby','-e',
        "require_relative 'scripts/read_rgss'; m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map763.rxdata'); puts JSON.generate([m.instance_variable_get(:@width),m.instance_variable_get(:@height)])"],
        cwd=ROOT,stderr=subprocess.DEVNULL))
    need(len(dimensions)==2 and 70<=dimensions[0]<200 and dimensions[1]>70,
         'Unreviewed Agate map dimensions')
    for mid,eid,pi in [(355,5,0),(355,118,0),(355,4,0),(365,3,2),(763,82,0),
                       (763,79,0),(752,7,0),(752,4,0),(752,8,0)]:
        e=event(mid,eid);p=e['pages'][pi]
        need(not any(c['code']==301 or 'pbTrainerBattle' in str(c['parameters'])
                     for c in p['list']), 'Assembly event gained a battle')
        proof.append({'map':mid,'event':eid,'page':pi,
                      'sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()})
    pc=event(355,5)
    need((pc['x'],pc['y'])==(38,24) and len(pc['pages'])==1
         and pc['pages'][0]['list'][0]['parameters']==[6,-1,8]
         and [c['parameters'] for c in pc['pages'][0]['list'] if c['code']==355]==[['pbPokeCenterPC']],
         'Circus PC must remain ordinary facing-Up access38,25')
    need(event(355,118)['pages'][0]['list'][0]['parameters']==[80], 'Circus recovery machine source changed')
    common=json.loads(subprocess.check_output(['ruby','-e',
        "require_relative 'scripts/read_rgss'; h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/CommonEvents.rxdata'); puts JSON.generate(plain(h[80]))"],
        cwd=ROOT,stderr=subprocess.DEVNULL))
    need([c['parameters'] for c in common['list'] if c['code']==314]==[[0]]
         and not any(c['code'] in [102,301] for c in common['list']),
         'Circus recovery must heal normally without a choice or battle')
    for mid,eid,pi,dest in [(355,4,0,[365,4,7]),(365,3,2,[763,13,54])]:
        page=event(mid,eid)['pages'][pi]
        need(page['trigger']==1 and
             [c['parameters'] for c in page['list'] if c['code']==201]==[[0,*dest,0,1]]
             and not any(c['code'] in [101,102,301] or 'pbTrainerBattle' in str(c['parameters'])
                         for c in page['list']), 'Normal external west-entry source changed')
    need(event(365,3)['pages'][2]['condition']['switch2_id']==988,
         'Restored Agate west-entry page condition changed')
    need(event(752,7)['pages'][0]['list'][0]['parameters']==['pbPokeCenterPC'] and
         event(752,4)['pages'][0]['list'][0]['parameters']==[1], 'Agate PC/nurse source changed')
    for mid,eid,dest in [(763,79,[752,10,10]),(752,8,[763,46,70])]:
        need([c['parameters'] for c in event(mid,eid)['pages'][0]['list'] if c['code']==201]
             ==[[0,*dest,0,1]], 'Agate center transfer changed')
    for eid,xy in [(41,(22,72)),(42,(22,73))]:
        e=event(763,eid);blank=e['pages'][1]
        need((e['x'],e['y'])==xy and blank['condition']['variable_valid'] and
             blank['condition']['variable_id']==391 and blank['condition']['variable_value']==52
             and not blank['graphic']['character_name'] and not blank['graphic']['tile_id'],
             'Installed west-entry stage51 barricade changed')
    setter=event(763,82)
    need((setter['x'],setter['y'])==(30,62) and setter['pages'][0]['trigger']==1
         and [(c['code'],c['parameters']) for c in setter['pages'][0]['list'] if c['code']!=0]
         ==[(122,[391,391,0,0,52])], 'Normal south-side stage setter changed')
    commitment=set()
    for eid in COMMIT_EVENTS:
        e=event(763,eid);p=e['pages'][0]
        need(e['y']==52 and p['trigger']==1 and
             [c['parameters'] for c in p['list'] if c['code']==122]==[[391,391,0,0,53]],
             'Gauntlet commitment strip changed')
        commitment.add((e['x'],e['y']))
    need(commitment=={(x,52) for x in range(43,49)}, 'Commitment strip geometry changed')
    storage=(GAME/'Scripts/Storage.rb').read_text()
    start=storage.index('  def pbStartBox(screen, command)')
    need('@selection = 0' in storage[start:start+900], 'Fresh PC cursor no longer starts0')
    pokemon=(GAME/'Scripts/Pokemon.rb').read_text()
    nature=pokemon[pokemon.index('  def nature\n'):pokemon.index('  def nature\n')+300]
    need('return @natureflag if @natureflag != nil' in nature,
         'Installed normal mint nature override changed')
    for eid in TRAINERS:
        e=event(763,eid);p=e['pages'][0]
        need(re.fullmatch(r'Trainer\(\d+\)',e['name']) and p['trigger']==2
             and p['move_type']==0, 'Agate trainer gained unreviewed automatic movement')
    return {'events':proof,'commitment':sorted(map(list,commitment)),'map_dimensions':dimensions,
            'fresh_box_cursor':0,'swap1':[1,11,1,'Kricketune','Tranquill'],
            'swap2':[1,6,1,'Hexan','Kricketune'],'normal_setter':[763,30,62],
            'assembly_pc':[355,5,38,25,'Up'],'recovery_common_event':80,
            'stop':[355,38,25],'approach_stop':[763,45,53],
            'fly_to_agate':False,'west_entry_stop':[763,13,54],
            'agate_assembly_pc':[752,7],'agate_assembly_stop':[763,46,70],
            'west_entry_requires_stage':52,
            'external_west_entry_separate':True}


def trainer_hazards(nav):
    hazards=set()
    for eid in TRAINERS:
        e=event(763,eid)
        for p in e['pages']:
            c=p['condition']
            for field in ['switch1','switch2']:
                if c[field+'_valid']:
                    need(type(nav.get('switches',{}).get(str(c[field+'_id']))) is bool,
                         'Explicit frozen trainer-page switch required')
            if c['self_switch_valid']:
                # Full checkpoint self-switch hash omits untouched false keys;
                # normal RGSS page selection treats an absent key as false.
                key=f"763,{eid},{c['self_switch_ch']}"
                need(key not in nav.get('self_switches',{}) or
                     type(nav['self_switches'][key]) is bool,'Malformed frozen trainer-completion flag')
        pi=selected_page(e,nav,763)
        if pi is None or e['pages'][pi]['trigger']!=2:
            continue
        p=e['pages'][pi];direction=p['graphic']['direction']
        need(direction in [2,4,6,8] and p['move_type']==0,'Unreviewed active trainer facing/movement')
        dx,dy={2:(0,1),4:(-1,0),6:(1,0),8:(0,-1)}[direction]
        n=int(re.fullmatch(r'Trainer\((\d+)\)',e['name'])[1])
        hazards.update((e['x']+i*dx,e['y']+i*dy) for i in range(n+1))
    return hazards


def preflight(status,nav,*,phase='assemble',incoming_lead='Cofagrigus',now=None):
    need(status.get('map')==(763 if phase in ['approach','agate-assemble'] else 355),
         'Frozen map differs from selected normal phase')
    p=status.get('party',[])
    if phase=='agate-assemble':
        need(len(p)==6 and set(m.get('species') for m in p)==set(START)
             and p[1].get('species')=='TRANQUILL' and p[0]['name']==incoming_lead,
             'Agate assembly requires reviewed travel six, carrier index1 and explicit actual lead')
    else:
        need(tuple(m.get('species') for m in p)==(START if phase=='assemble' else FINAL),
             'Party order differs from reviewed phase six')
    need(len({m['name'] for m in p})==6,'Unique actual party names required')
    cf=next(m for m in p if m['species']=='COFAGRIGUS')
    need(cf['name']=='Cofagrigus' and cf['level']==90 and effective_nature(cf)=='TIMID'
         and cf['ev']==CF_EV and [m['move'] for m in cf['moves']]==CF_MOVES,
         'Finish the exact normal Cofa build/training first')
    need([cf[k] for k in ['totalhp','attack','defense','spatk','spdef','speed']]
         ==[252,93,333,210,218,68] and cf.get('item') in [None,'POWERLENS'],
         'Cofa measured stats/item differ')
    if phase in ['assemble','agate-assemble']:
        need(p[1]['name']=='Tranquill' and p[1]['hp']>0
             and 'FLY' in {m['move'] for m in p[1]['moves']},'Owned conscious Fly carrier required')
        if phase=='agate-assemble':
            # This is a source-excluded walk into the normal PC, followed by
            # an explicit ordinary nurse heal. Ricardo may leave living travel
            # members injured; initial full HP adds an unnecessary extra heal.
            # Status and consciousness remain guarded below, and final native
            # full HP/status/PP proof is unchanged.
            need(cf.get('item') is None and all(0<m['hp']<=m['totalhp'] for m in p),
                 'Agate assembly requires no Lens and conscious travel six')
            need(len(status['position'])==2 and status['position'][1]>=53,
                 'Agate assembly must start south of the commitment strip')
    else:
        need(cf.get('item') is None and p[5]['name']=='Hexan' and p[5].get('item')=='FOCUSSASH',
             'Approach requires the already assembled Cofa/Hexan items')
        need(all(m['level']==90 and m['hp']==m['totalhp'] for m in p),
             'Heal the actual final six before the standalone approach')
        if phase=='west-entry':
            need(nav.get('switches',{}).get('988') is True,
                 'West entry requires actual restored Agate switch988=True')
    need(all(m['hp']>0 and m['status'] is None for m in p),'Healthy conscious travel party required')
    stage=nav.get('variables',{}).get('391')
    need(stage in [51,52],'Only reviewed pre-Agate stages51/52 are allowed')
    need(phase not in ['west-entry','agate-assemble'] or stage==52,
         'Stage51 Agate west/Fly plateau is barricaded: retain Tranquill and take the reviewed Vanhanen→south approach first')
    need(nav.get('switches',{}).get('5') is False,'Unreviewed center nurse autorun page')
    hazards=trainer_hazards(nav)
    need(phase!='approach' or stage!=51 or (30,62) not in hazards,
         'Normal stage52 setter is inside an unbeaten active trainer sightline; stop for a separate reviewed encounter')
    if now is not None:
        saved=datetime.fromisoformat(status['save_mtime']).timestamp()
        need(-5<=now-saved<=300,'Explicit normal start checkpoint must be at most300s old')
    return {'phase':phase,'initial_stage':stage,'incoming_lead':incoming_lead,
            'trainer_hazards':sorted(map(list,hazards)),
            'optional_setter_blocked':stage==51 and (30,62) in hazards,
            'remove_lens':cf.get('item')=='POWERLENS'}


def card_slot(rows,name):
    hits=[]
    for r in rows:
        if norm(r['text'])!=norm(name) or not .1<r['y']<.7:
            continue
        col=int(r['x']>.5);row=round((r['y']-(.15 if not col else .195))/.21)
        if row in [0,1,2]:hits.append(row*2+col)
    need(len(hits)==1,'Actual named party card is not unique: '+name)
    return hits[0]


def final_proof(before,after,nav,maxima,*,phase='approach',initial_stage=52):
    endpoint=[38,25] if phase=='assemble' else ([46,70] if phase=='agate-assemble' else [45,53])
    stage=initial_stage if phase=='assemble' else 52
    need(after['map']==(355 if phase=='assemble' else 763) and after['position']==endpoint
         and nav['variables'].get('391')==stage,'Final safe coordinate/stage not proven')
    party=after['party']
    need(tuple(m['species'] for m in party)==FINAL,'Final fixed-six order differs')
    need(all(m['level']==90 and m['hp']==m['totalhp'] and m['status'] is None for m in party),
         'Every final member must be level90, full HP and status-free')
    need(all(move['pp']==full_pp(move,maxima) for mon in party for move in mon['moves']),
         'Final normal nurse did not prove full PP')
    cf=party[0]
    need(cf.get('item') is None and cf['ev']==CF_EV and effective_nature(cf)=='TIMID'
         and [m['move'] for m in cf['moves']]==CF_MOVES,'Final Cofa build/Lens removal differs')
    cryo=party[5]
    need(cryo['name']=='Hexan' and cryo['item']=='FOCUSSASH','Hexan must actually hold the borrowed Sash')
    old={m['species']:m for m in before['party']}
    for mon in party[:5] if phase in ['assemble','agate-assemble'] else party:
        expected=dict(old[mon['species']])
        if mon['species']=='COFAGRIGUS':expected['item']=None
        need(all(mon.get(k)==expected.get(k) for k in IDENTITY),
             'Travel changed a retained member: '+mon['name'])
        need([m['move'] for m in mon['moves']]==[m['move'] for m in expected['moves']],
             'Retained moves changed during assembly')
    need(after['trainer']['money']==before['trainer']['money'],'Unexpected spending during PC assembly')
    contents=before['bag']['contents'];new=after['bag']['contents']
    need(new.get('FOCUSSASH',0)==contents.get('FOCUSSASH',0),'Sash take/give quantity did not reconcile')
    need(new.get('POWERLENS',0)==contents.get('POWERLENS',0)+int(old['COFAGRIGUS'].get('item')=='POWERLENS'),
         'Power Lens removal did not reconcile')
    for key in ['ULTRAPOTION','FULLHEAL','XSPEED','XDEFEND','XATTACK','XSPECIAL','XSPDEF','REVIVALHERB']:
        need(new.get(key,0)==contents.get(key,0),'Unexpected medicine use during assembly: '+key)


class Runner(Base):
    def __init__(self,args,status,nav,proposal):
        self.args=args;self.path=args.journal.resolve();self.status=status
        need(self.path.is_relative_to(ROOT) and not self.path.exists(),'NEW workspace journal required; no replay')
        self.work=ROOT/'work'/self.path.stem
        need(not self.work.exists(),'Evidence directory already exists; review instead of replay')
        self.work.mkdir();self.started=time.time()
        self.journal={'source_proof':source_proof(),'frozen_status_sha256':digest(args.status),
                      'frozen_navigation_sha256':digest(args.navigation),'proposal':proposal,
                      'events':[],'pending':None,'screens':[]}
        self.expected=[m['name'] for m in status['party']]
        self.write()

    def health(self):
        need(time.time()-self.started<1800,'Assembly exceeded30-minute bound; stop for review')
        h=json.loads((ROOT/'recordings/capture-health.json').read_text())
        need(h.get('active') is True and -2<=time.time()-h.get('epoch',0)<2,
             'Recording is not fresh; no queue action')
        return h

    def same(self,a):
        b=self.health()
        need((a.get('pid'),a.get('restart_count',0))==(b.get('pid'),b.get('restart_count',0)),
             'Capture restarted; stop and review actual endpoint, never replay')

    def keys(self,*keys):
        from play import act
        before=self.health();self.journal['pending']={'keys':list(keys),'epoch':time.time()};self.write()
        act(*keys);self.same(before);self.record('ordinary-keys-returned',keys=list(keys))
        self.journal['pending']=None;self.write()

    def run(self,script,*args):
        args=tuple(str(value) if isinstance(value,Path) else value for value in args)
        before=self.health();self.journal['pending']={'script':script,'args':list(args),'epoch':time.time()};self.write()
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*map(str,args)],
                              capture_output=True,text=True,timeout=240)
        self.record('ordinary-helper-diagnostic',script=script,args=list(args),returncode=result.returncode,stdout=result.stdout,stderr=result.stderr)
        need(result.returncode==0,'Ordinary helper stopped: '+result.stderr[-1500:])
        self.same(before);print(result.stdout,flush=True)
        self.record('ordinary-helper-returned',script=script,args=list(args),stdout=result.stdout)
        self.journal['pending']=None;self.write();return result.stdout

    def public(self,*,game_rows=False):
        from play import snap,NATIVE
        from PIL import Image
        before=self.health();need(len(self.journal['screens'])<80,'Bounded public capture limit')
        rows=snap();native=Image.open(NATIVE).convert('RGB')
        path=self.work/f'public-{len(self.journal["screens"])}.png';native.save(path)
        record={'epoch':time.time(),'image':str(path),'rows':rows}
        game=None
        if game_rows:
            canvas=CANVASES.get(native.size);need(canvas is not None,'Uncalibrated capture canvas')
            l,t,w,h=canvas;game=native.crop((l,t,l+w,t+h)).resize((512,384),Image.Resampling.NEAREST)
            crop=path.with_name(path.stem+'-game.png');game.resize((1536,1152),Image.Resampling.NEAREST).save(crop)
            rows=json.loads(subprocess.check_output([str(ROOT/'scripts/observe_words'),str(crop)],timeout=20))
            record.update(game_image=str(crop),game_rows=rows,canvas=list(canvas))
        self.same(before);self.journal['screens'].append(record);self.write();return rows,game

    def settle(self):
        rows,_=self.public(game_rows=True)
        labels={norm(r['text']) for r in rows}
        if {'bag','controls','quitgame'}<=labels and labels&{'options','uptions'}:
            self.keys('x:.12','wait:.6')
        self.world()

    def open_pause_choice(self,name):
        from PIL import Image
        self.world();self.keys('x:.12','wait:.6')
        rows,game=self.public(game_rows=True);pause_guard(rows)
        target=unique_label(rows,name,side='right')
        template=Image.open(GAME/'Graphics/Pictures/selarrow.png').convert('RGBA')
        arrow=find_arrow(game,template,(256,0,512,384));steps=alignment(target,arrow)
        if steps:self.keys(*(['down:.12' if steps>0 else 'up:.12']*abs(steps)),'wait:.3')
        rows,game=self.public(game_rows=True);pause_guard(rows)
        need(alignment(unique_label(rows,name,side='right'),find_arrow(game,template,(256,0,512,384)))==0,
             'Actually selected Pause command differs; no C sent')
        self.keys('c:.12','wait:1.2')

    def party_check(self):
        self.open_pause_choice('Pokémon');rows,_=self.public()
        need(all(card_slot(rows,name)==slot for slot,name in enumerate(self.expected)),
             'Actual party cards differ after exchange')
        self.keys('x:.12','wait:.5');self.settle()
        self.record('actual-party-order-verified',names=list(self.expected))

    def take(self,name,item):
        self.open_pause_choice('Pokémon');rows,_=self.public()
        need(card_slot(rows,name)==self.expected.index(name),'Expected item owner is not in actual party')
        self.run('party_pick',name,'--single')
        out=self.run('take_held',name,item,'--menu-open')
        need(norm(item) in norm(out) and norm(name) in norm(out),'Named held-item receipt missing')
        self.settle();self.record('visible-held-item-taken',owner=name,item=item)

    def exchange(self,slot,incoming,outgoing):
        from play import read
        mid,eid=(752,7) if self.args.phase=='agate-assemble' else (355,5)
        self.position(mid);self.active_source(mid,eid,0)
        self.run('eventq',mid,eid,'talk');self.run('pc_open_reviewed')
        need(re.search(r'\bbox\s*1\b',read().lower()),'Fresh Box1 required; no exchange keys sent')
        out=self.run('pc_exchange_named',slot,1,incoming,outgoing)
        need('EXCHANGE COMPLETE '+incoming+' '+outgoing in out,'Exchange completion receipt missing')
        self.expected[1]=incoming;self.settle();self.position(mid);self.party_check()

    def arrange(self,order=FINAL):
        from play import snap,STATE
        from party_cursor import selected_card,selection_path
        names={m['species']:m['name'] for m in self.status['party']};names['CRYOGONAL']='Hexan'
        wanted=[names[s] for s in order]
        self.open_pause_choice('Pokémon')
        for dest,name in enumerate(wanted):
            rows,_=self.public();source=card_slot(rows,name)
            if source==dest:continue
            steps=selection_path(selected_card(STATE),dest)
            if steps:self.keys(*steps,'wait:.3');snap()
            need(selected_card(STATE)==dest,'Actual party source cursor differs')
            self.keys('a:.12','wait:.4',*selection_path(dest,source),'wait:.3');snap()
            need(selected_card(STATE)==source,'Actual party swap destination differs')
            self.keys('c:.12','wait:1.2');rows,_=self.public()
            need(card_slot(rows,name)==dest,'Actual party swap result differs')
        self.expected=wanted;rows,_=self.public()
        need(all(card_slot(rows,n)==i for i,n in enumerate(wanted)),'Final visible party order differs')
        self.keys('x:.12','wait:.5');self.settle()

    def hard_avoid(self,nav):
        state=self.nav();need(state['variables'].get('391')==nav['variables'].get('391'),
                              'Current planner story stage differs from frozen checkpoint')
        hazards=trainer_hazards(state)
        # Block the entire latitude, so even a detouring path cannot go north
        # around one edge of the actual six-tile commitment strip.
        width=source_proof()['map_dimensions'][0]
        previous=set(map(tuple,state.get('avoid',{}).get('763',[])))
        introduced=set(map(tuple,state.get('agate_party_owned_avoid',[])))
        original=previous-introduced
        desired=hazards|{(x,52) for x in range(width)}
        blocked=original|desired
        state.setdefault('avoid',{})['763']=sorted(map(list,blocked))
        # Remove only this queue's own prior exclusions when actual trainer
        # completion has changed; preserve any independently owned obstacles.
        state['agate_party_owned_avoid']=sorted(map(list,desired-original))
        (ROOT/'notes/navigation-state.json').write_text(json.dumps(state)+'\n')
        self.record('source-hazards-hard-excluded-from-planner',tiles=sorted(map(list,blocked)))

    def walk(self,x,y):
        need(y>=53,'Queue may not cross the gauntlet commitment latitude')
        actual=self.position(763);p=self.work/'route-next.json'
        p.write_text(json.dumps([[763,actual[1],actual[2],x,y,[]]]))
        self.run('queue_route',p,'--from-verified');self.position(763,(763,x,y))

    def checkpoint_proof(self,proposal):
        self.run('checkpoint',self.args.checkpoint)
        status_path=ROOT/'notes'/f'{self.args.checkpoint}-status.json'
        nav_path=ROOT/'notes'/f'{self.args.checkpoint}-navigation.json'
        need(status_path.stat().st_mtime>=self.started and nav_path.stat().st_mtime>=self.started,
             'Final checkpoint evidence is stale')
        code="require_relative 'scripts/read_rgss'; h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/moves.dat'); puts JSON.generate(h.transform_values{|m|m.instance_variable_get(:@maxpp)})"
        maxima=json.loads(subprocess.check_output(['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))
        final_proof(self.status,json.loads(status_path.read_text()),json.loads(nav_path.read_text()),maxima,
                    phase=self.args.phase,initial_stage=proposal['initial_stage'])
        self.journal.update(status='completed-safe-phase',verified=True,final_status_sha256=digest(status_path),
                            final_navigation_sha256=digest(nav_path));self.write()

    def assemble(self,nav,proposal):
        from play import read
        self.position(355,(355,*self.status['position']));self.party_check()
        if proposal['remove_lens']:self.take('Cofagrigus','Power Lens')
        self.exchange(11,'Kricketune','Tranquill');self.take('Kricketune','Focus Sash')
        self.exchange(6,'Hexan','Kricketune')
        self.open_pause_choice('Bag')
        self.run('give_held','Focus Sash','Hexan','--bag-open');self.settle();self.arrange()
        self.active_source(355,118,0);self.run('eventq',355,118,'talk')
        welcome=norm(read());need('recoveryunitinitiated' in welcome or 'fullyhealed' in welcome,
                                  'Expected normal Circus recovery message')
        self.run('heal');self.position(355)
        self.run('q','355,38,25');self.position(355,(355,38,25))
        self.party_check();self.position(355,(355,38,25));self.stage(proposal['initial_stage'])
        self.checkpoint_proof(proposal)
        print('CIRCUS FINAL SIX READY355[38,25]; stage'+str(proposal['initial_stage'])+
              '. West entry is disabled before52; current approved plan retains Fly for Vanhanen→south instead.',flush=True)

    def agate_assemble(self,nav,proposal):
        from play import read
        self.position(763,(763,*self.status['position']));self.stage(52);self.party_check()
        # Explicitly observed incoming lead may be Swampert after the defender
        # fights. Restore the named travel order before the fixed index1 swaps.
        self.arrange(START);self.hard_avoid(nav);self.active_source(763,79,0)
        self.run('eventq',763,79,'enter');self.position(752,(752,10,10))
        self.exchange(11,'Kricketune','Tranquill');self.take('Kricketune','Focus Sash')
        self.exchange(6,'Hexan','Kricketune');self.open_pause_choice('Bag')
        self.run('give_held','Focus Sash','Hexan','--bag-open');self.settle();self.arrange()
        self.active_source(752,4,0);self.run('eventq',752,4,'talk')
        welcome=read().lower();need('welcome' in welcome or 'rest' in welcome,'Expected ordinary Agate nurse welcome')
        self.run('choose_dialog','Yes|No','Yes');self.run('heal');self.position(752)
        self.active_source(752,8,0);self.run('eventq',752,8,'enter')
        self.position(763,(763,46,70));self.party_check();self.stage(52)
        self.position(763,(763,46,70));self.checkpoint_proof(proposal)
        print('AGATE FINAL SIX SOUTH READY763[46,70] stage52; no gauntlet commitment sent.',flush=True)

    def approach(self,nav,proposal):
        self.position(763,(763,*self.status['position']));self.party_check();self.hard_avoid(nav)
        if proposal['initial_stage']==51:
            need((30,62) not in trainer_hazards(self.nav()),'Stage setter is in an active trainer sightline')
            self.active_source(763,82,0);self.walk(30,63);self.walk(30,62)
            # Public exact arrival + clear overworld prove stepping on the sole
            # unconditional setter. Mirror its completed effect to notes only.
            self.mirror(763,82,0);self.stage(52)
        self.walk(45,53);self.stage(52);self.party_check();self.position(763,(763,45,53))
        self.checkpoint_proof(proposal)
        print('AGATE FIXED SIX VERIFIED763[45,53] stage52; no gauntlet commitment sent.',flush=True)

    def west_entry(self,nav,proposal):
        self.position(355,(355,*self.status['position']));self.party_check()
        self.active_source(355,4,0);self.run('eventq',355,4,'enter')
        self.position(365,(365,4,7));self.mirror(355,4,0)
        self.active_source(365,3,2);self.run('eventq',365,3,'enter')
        self.position(763,(763,13,54));self.mirror(365,3,2)
        self.stage(proposal['initial_stage'])
        self.journal.update(status='completed-safe-west-entry',verified=True,
                            actual_stop=[763,13,54],no_additional_save=True);self.write()
        print('AGATE WEST ENTRY VERIFIED763[13,54]; STOP before street defenders. No battle or additional save sent.',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase',choices=['assemble','agate-assemble','west-entry','approach'],default='assemble')
    p.add_argument('--incoming-lead',choices=['Cofagrigus','Swampert'],default='Cofagrigus')
    p.add_argument('--status',type=Path);p.add_argument('--navigation',type=Path)
    p.add_argument('--execute',action='store_true')
    p.add_argument('--journal',type=Path,default=ROOT/'work/agate-party-assemble-129.json')
    p.add_argument('--checkpoint')
    args=p.parse_args();proposal={'proposal':True,'executed':False,'source':source_proof(),
        'sequence':['optional take Cofa Lens','Circus355E5 freshPC swap11→party1 Kricketune',
                    'take Kricketune Sash','freshPC swap6→party1 Hexan','give Hexan Sash',
                    'arrange CF/Arc/Swamp/Mien/Exc/Hexan','normal Circus recovery355E118',
                    'stop35538,25','single Circus-final-six-ready129 checkpoint'],
        'optional_approach':['after separate actual trainer review/heal/freshcheckpoint',
                    'if stage51 and source-safe: normal763E82 setter','stop76345,53','single prechain checkpoint'],
        'optional_west_entry':['afterCircus finalsixproof','355E4→3654,7','365E3page2→76313,54',
                    'REQUIRESstage52; stage51barricaded','stopbeforestreetdefenders','noadditionalcheckpoint'],
        'agate_assemble':['retainTranquillthroughsouthernentry+Ricardo','fresh763stage52consciousstatusfreeTravel6',
                    'namedCFfront','PC752swaps11then6','giveHexanSash','reorderfinalsix','normalnurse',
                    'singlecheckpoint76346,70stage52']}
    args.checkpoint=args.checkpoint or ('Circus-final-six-ready129' if args.phase=='assemble' else
                                      'Agate-final-six-south-ready130' if args.phase=='agate-assemble' else
                                      'Agate-fixed-six-ready129')
    proposal['selected_phase']=args.phase
    if args.phase!='assemble':
        proposal['sequence']=proposal[{'agate-assemble':'agate_assemble',
                                      'west-entry':'optional_west_entry','approach':'optional_approach'}[args.phase]]
    status=nav=None
    if args.status or args.navigation:
        need(args.status and args.navigation,'Pass both explicit frozen evidence paths')
        need(args.status.resolve().is_relative_to(ROOT) and args.navigation.resolve().is_relative_to(ROOT),
             'Frozen evidence must be in workspace')
        status=json.loads(args.status.read_text());nav=json.loads(args.navigation.read_text())
        proposal.update(preflight(status,nav,phase=args.phase,incoming_lead=args.incoming_lead,
                                  now=time.time() if args.execute else None))
    print(json.dumps(proposal,indent=2),flush=True)
    if not args.execute:return
    need(status is not None,'--execute requires explicit frozen --status and --navigation')
    need(re.fullmatch(r'[A-Za-z0-9_-]+',args.checkpoint),'Invalid checkpoint label')
    if args.phase!='west-entry':
        need(not (ROOT/'notes'/f'{args.checkpoint}-status.json').exists(),'Final checkpoint already exists; no replay')
    runner=Runner(args,status,nav,proposal)
    try:getattr(runner,args.phase.replace('-','_'))(nav,proposal)
    except BaseException as error:
        runner.journal.update(status='stopped-for-actual-state-review',verified=False)
        runner.record('stop',reason=str(error),error=type(error).__name__);raise


if __name__=='__main__':main()
