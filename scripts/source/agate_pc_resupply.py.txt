"""Finite normal Agate PC→Dept8F→Agate supply trip; dry-run by default.

Only explicit --execute uses public controls or makes the single final normal
checkpoint. No battle is intentionally started; partial journals are not
resumed/replayed. Use an explicit completed-street frozen checkpoint.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from datetime import datetime
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
from agate_party_assemble import (Runner as AssemblyRunner, FINAL, IDENTITY,
    CF_EV, CF_MOVES, effective_nature, source_proof as assembly_source)
from agate_archive_core import full_pp
from agate_supply_queue import vendor_ready_public
from calcenon_agate_queue import event, need, selected_page

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Applications/Reborn.app/Contents/Game')
CART=(('XSPECIAL','X Sp. Atk',4,350),('XSPEED','X Speed',3,350),
      ('XACCURACY','X Accuracy',2,950))
COST=sum(q*p for _,_,q,p in CART)


@lru_cache(maxsize=1)
def source_event_geometry():
    # Static asset metadata only, no route_map/native reads. Lists are omitted.
    code="""require_relative 'scripts/read_rgss'; m=load_rgss('/Applications/Reborn.app/Contents/Game/Data/Map763.rxdata'); h=m.instance_variable_get(:@events); puts JSON.generate(h.transform_values{|e|q=plain(e); q['pages'].each{|p|p.delete('list')}; q})"""
    return json.loads(subprocess.check_output(['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))


def clear_completed_street_rays(nav):
    """Pure, narrow stale-planner cleanup after all three proven victories.

    Only original E45/46/49 source ray cells beyond each NPC are eligible.
    Original NPC tiles, current saved visible NPC positions, commitment52 and
    every other avoid remain.
    This returns notes data only; no native/game/save changes are made.
    """
    need(nav.get('variables',{}).get('391')==52 and
         all(nav.get('self_switches',{}).get(f'763,{e},A') is True for e in [45,46,49]),
         'Completed-street cleanup requires actual52 + all45/46/49victories')
    positions=nav.get('positions',{}).get('763',{})
    need(all(str(e) in positions for e in [45,46,49]),
         'Frozen/current normal checkpoint must include actual street NPC positions')
    protected=set()
    for key,e in source_event_geometry().items():
        pi=selected_page(e,nav,763)
        if pi is None:continue
        page=e['pages'][pi];graphic=page['graphic']
        if (graphic.get('character_name') or graphic.get('tile_id')) and not page.get('through'):
            protected.add(tuple(positions.get(key,[e['x'],e['y']])))
    eligible=set()
    for eid,xy,direction in [(45,(42,60),8),(46,(42,55),2),(49,(37,63),8)]:
        e=event(763,eid);p=e['pages'][0]
        need((e['x'],e['y'])==xy and e['name']=='Trainer(4)' and p['trigger']==2
             and p['move_type']==0 and p['graphic']['direction']==direction,
             'Reviewed original street footprint changed')
        active=selected_page(e,nav,763)
        need(active is not None and e['pages'][active]['trigger']!=2,
             'An actual street trainer page is still active')
        dy=-1 if direction==8 else 1
        eligible.update((xy[0],xy[1]+i*dy) for i in range(1,5))
    old=set(map(tuple,nav.get('avoid',{}).get('763',[])))
    removed=(old & eligible)-protected
    result=deepcopy(nav)
    result.setdefault('avoid',{})['763']=sorted(map(list,old-removed))
    result['agate_completed_street_guard_cleanup']={
        'completed_events':[45,46,49],'removed':sorted(map(list,removed)),
        'retained_current_npc_positions':sorted(map(list,protected & eligible)),
        'source_original_footprints':sorted(map(list,eligible)),
        'policy':'planning only; actual NPCs/other avoids/commitment preserved'}
    return result,result['agate_completed_street_guard_cleanup']


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def source_proof():
    facts=assembly_source()
    shop=event(4,4)
    need(len(shop['pages'])==1 and (shop['x'],shop['y'])==(5,5),
         'Unreviewed Xitem merchant geometry/pages')
    page=shop['pages'][0]
    need(not any(page['condition'][k] for k in
         ['switch1_valid','switch2_valid','variable_valid','self_switch_valid']),
         'Xitem merchant gained a gated page')
    script='\n'.join(str(c['parameters'][0]) for c in page['list'] if c['code'] in [355,655])
    need('pbPokemonMart' in script and all(':'+k in script for k,_,_,_ in CART)
         and not any(c['code'] in [102,301] for c in page['list']),
         'Source Xitem stock/dialogue changed')
    itemtext=(GAME/'Scripts/Reborn/itemtext.rb').read_text()
    for key,label,qty,price in CART:
        block=re.search(r'(?m)^\s*:'+key+r'\s*=>\s*\{(.*?)\n\s*\},',itemtext,re.S)
        need(block and re.search(r':price\s*=>\s*'+str(price)+r'\b',block[1]),
             'Installed item price changed: '+label)
    facts.update(cart=[{'item':k,'label':n,'quantity':q,'unit_price':p} for k,n,q,p in CART],
                 cost=COST,box1_slot=11,party_slot=5,shop=[4,4],
                 stop=[763,46,70],source_only_no_controls=True)
    return facts


def preflight(status,nav,*,now=None):
    need(status.get('map')==763 and len(status.get('position',[]))==2 and
         status['position'][1]>=53,'Start from a frozen normal south-Agate checkpoint')
    need(nav.get('variables',{}).get('391')==52,'Only prechain story39152 accepted')
    need(all(nav.get('self_switches',{}).get(f'763,{e},A') is True for e in [45,46,49]),
         'Explicit completed Lyla/Ezra/Antoine victory flags required')
    need(nav.get('switches',{}).get('5') is False and
         nav.get('switches',{}).get('988') is True,'Reviewed nurse/Agate entry flags required')
    need(nav['variables'].get('175',-1)>=7 and
         status['bag']['contents'].get('MEMBERSHIPCARD',0)>=1,'Normal Dept8F membership required')
    need(status['trainer']['badges'].count(True)==16,'Expected16badges before Agate chain')
    party=status.get('party',[])
    need(len(party)==6 and {m.get('species') for m in party}==set(FINAL)
         and len({m['name'] for m in party})==6,'Exact reviewed six with unique names required')
    need(all(m['level']==90 and 0<=m['hp']<=m['totalhp'] for m in party),
         'Reviewed six must remain Lv90 with valid frozen HP; normal nurse heals injuries')
    cf=next(m for m in party if m['species']=='COFAGRIGUS')
    need(cf['name']=='Cofagrigus' and effective_nature(cf)=='TIMID' and
         cf.get('item') is None and cf['ev']==CF_EV and
         [m['move'] for m in cf['moves']]==CF_MOVES and
         [cf[k] for k in ['totalhp','attack','defense','spatk','spdef','speed']]==
         [252,93,333,210,218,68],'Frozen normal Cofa build differs')
    cryo=next(m for m in party if m['species']=='CRYOGONAL')
    need(cryo['name']=='Hexan' and cryo.get('item')=='FOCUSSASH',
         'Actual Hexan must still hold Sash; no consumed item is re-created')
    need(status['trainer']['money']>=COST,'Actual frozen money insufficient for4350cart')
    if now is not None:
        saved=datetime.fromisoformat(status['save_mtime']).timestamp()
        need(-5<=now-saved<=300,'Execution requires a fresh normal checkpoint≤300s old')
    _,cleanup=clear_completed_street_rays(nav)
    return {'initial_stage':52,'initial_party_order':[m['species'] for m in party],
            'temporary_carrier':'Tranquill','box1_slot':11,'party_slot':5,
            'total_cost':COST,'expected_money':status['trainer']['money']-COST,
            'final_position':[763,46,70],'source_reviewed_stale_ray_cleanup':cleanup}


def final_proof(before,after,nav,maxima,*,expected_position=(46,70)):
    need(tuple(expected_position) in {(46,70),(45,53)}, 'Only reviewed south/prechain endpoints accepted')
    need(after['map']==763 and after['position']==list(expected_position) and
         nav['variables'].get('391')==52,'Final safe southern coordinate/stage differs')
    need(tuple(m['species'] for m in after['party'])==FINAL,'Final six order differs')
    old={m['species']:m for m in before['party']}
    for mon in after['party']:
        prior=old[mon['species']]
        need(all(mon.get(k)==prior.get(k) for k in IDENTITY),
             'Normal trip changed retained identity/held item: '+mon['name'])
        need([m['move'] for m in mon['moves']]==[m['move'] for m in prior['moves']],
             'Retained moves changed: '+mon['name'])
        need([m.get('ppup',0) for m in mon['moves']]==
             [m.get('ppup',0) for m in prior['moves']],
             'Retained PP Up investment changed: '+mon['name'])
        need(mon['level']==90 and mon['hp']==mon['totalhp'] and mon['status'] is None,
             'Final nurse must prove full HP/status-free Lv90 party')
        need(all(m['pp']==full_pp(m,maxima) for m in mon['moves']),
             'Final nurse full PP proof missing')
    need(after['trainer']['money']==before['trainer']['money']-COST,
         'Normal shop money does not reconcile4350')
    expected=dict(before['bag']['contents'])
    for key,_,q,_ in CART:expected[key]=expected.get(key,0)+q
    actual=after['bag']['contents']
    need({k:v for k,v in expected.items() if v}=={k:v for k,v in actual.items() if v},
         'Exact final bag delta must be purchases only; Sash stays with boxed Cryo')
    need(actual.get('XSPECIAL',0)>=6 and actual.get('XSPEED',0)>=3,
         'Insufficient restored chain setup stock')


class Runner(AssemblyRunner):
    def run(self,script,*args):
        # Base world() handles a visible expired-Repel prompt. This town-only
        # trip needs no wild protection; cancel it normally so bag accounting
        # remains exactly the reviewed shop cart.
        if script=='renew_repel':
            need(not args,'Unexpected inherited Repel renewal arguments')
            args=('--cancel',)
        return super().run(script,*args)

    def exchange_carrier(self,incoming,outgoing):
        from play import read
        self.position(752);self.active_source(752,7,0)
        self.run('eventq',752,7,'talk');self.run('pc_open_reviewed')
        need(re.search(r'\bbox\s*1\b',read().lower()),'Fresh Box1 required; no swap keys sent')
        out=self.run('pc_exchange_named',11,5,incoming,outgoing)
        need('EXCHANGE COMPLETE '+incoming+' '+outgoing in out,'Named exchange receipt missing')
        self.expected[5]=incoming;self.settle();self.position(752);self.party_check()

    def nurse(self):
        from play import read
        self.position(752);self.active_source(752,4,0)
        self.run('eventq',752,4,'talk')
        welcome=read().lower();need('welcome' in welcome or 'rest' in welcome,'Normal nurse greeting required')
        self.run('choose_dialog','Yes|No','Yes');self.run('heal');self.position(752)

    def trip(self,nav,proposal):
        self.position(763,(763,*self.status['position']));self.stage(52)
        self.party_check()
        cleaned,proof=clear_completed_street_rays(self.nav())
        (ROOT/'notes/navigation-state.json').write_text(json.dumps(cleaned)+'\n')
        self.record('completed-street-source-ray-guards-cleared',proof=proof)
        self.hard_avoid(nav)
        self.active_source(763,79,0);self.run('eventq',763,79,'enter');self.position(752,(752,10,10))
        self.nurse();self.arrange();self.exchange_carrier('Tranquill','Hexan')
        self.active_source(752,8,0);self.run('eventq',752,8,'enter');self.position(763,(763,46,70))
        self.run('fly_to',520,'--carrier','Tranquill');self.position(520)
        for mid,eid,mode,dest in [(520,101,'enter',112),(112,6,'enter',113)]:
            self.run('eventq',mid,eid,mode);self.position(dest)
        self.run('eventq',113,1,'talk');self.run('dept_greet');self.run('dept_floor',8);self.position(4)
        self.active_source(4,4,0);self.run('eventq',4,4,'talk');vendor_ready_public()
        self.run('mart_open')
        for _,name,q,p in CART:self.run('shop_buy',name,q,p)
        self.run('mart_exit');self.position(4)
        self.run('eventq',4,6,'enter');self.position(113)
        self.run('eventq',113,1,'talk');self.run('dept_greet');self.run('dept_floor',1);self.position(112)
        self.run('eventq',112,1,'enter');self.position(520)
        self.run('fly_to',763,'--carrier','Tranquill');self.position(763,(763,46,70));self.stage(52)
        self.active_source(763,79,0);self.run('eventq',763,79,'enter');self.position(752,(752,10,10))
        self.exchange_carrier('Hexan','Tranquill');self.arrange();self.nurse()
        self.active_source(752,8,0);self.run('eventq',752,8,'enter');self.position(763,(763,46,70))
        self.party_check();self.stage(52);self.position(763,(763,46,70))
        self.run('checkpoint',self.args.checkpoint)
        sp=ROOT/'notes'/f'{self.args.checkpoint}-status.json'
        np=ROOT/'notes'/f'{self.args.checkpoint}-navigation.json'
        need(sp.stat().st_mtime>=self.started and np.stat().st_mtime>=self.started,'Final evidence is stale')
        code="require_relative 'scripts/read_rgss'; h=load_rgss('/Applications/Reborn.app/Contents/Game/Data/moves.dat'); puts JSON.generate(h.transform_values{|m|m.instance_variable_get(:@maxpp)})"
        maxima=json.loads(subprocess.check_output(['ruby','-e',code],cwd=ROOT,stderr=subprocess.DEVNULL))
        final_proof(self.status,json.loads(sp.read_text()),json.loads(np.read_text()),maxima)
        self.journal.update(status='completed-safe-supply-trip',verified=True,
                            final_status_sha256=digest(sp),final_navigation_sha256=digest(np));self.write()
        print('AGATE RESTOCKED4350; fixed six fullHP/PP763[46,70] stage52. No chain commitment.',flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--status',type=Path);p.add_argument('--navigation',type=Path)
    p.add_argument('--execute',action='store_true');p.add_argument('--journal',type=Path,
        default=ROOT/'work/agate-pc-resupply.json')
    p.add_argument('--checkpoint',default='Agate-restocked-south-ready131')
    args=p.parse_args();args.phase='agate-assemble'
    proposal={'proposal':True,'executed':False,'source':source_proof(),
              'sequence':['require45/46/49victories39152','normal752nurse',
                'arrangefixedsix','Box1slot11Tranquill→Cryoparty5 preservingSash',
                'Fly520→normalDept8F','buy4SpAtk3Speed2Acc4350','Fly763south',
                'restore exactCryoslot11→party5','normalnurse','single finalcheckpoint76346,70']}
    status=nav=None
    if args.status or args.navigation:
        need(args.status and args.navigation,'Pass both explicit frozen paths')
        need(args.status.resolve().is_relative_to(ROOT) and args.navigation.resolve().is_relative_to(ROOT),
             'Frozen evidence must be workspace files')
        status=json.loads(args.status.read_text());nav=json.loads(args.navigation.read_text())
        proposal.update(preflight(status,nav,now=time.time() if args.execute else None))
    print(json.dumps(proposal,indent=2),flush=True)
    if not args.execute:return
    need(status is not None,'--execute requires explicit completed-street frozen evidence')
    need(re.fullmatch(r'[A-Za-z0-9_-]+',args.checkpoint),'Invalid checkpoint label')
    need(not (ROOT/'notes'/f'{args.checkpoint}-status.json').exists() and
         not (ROOT/'notes'/f'{args.checkpoint}-navigation.json').exists(),
         'Final checkpoint exists; no replay/overwrite')
    runner=Runner(args,status,nav,proposal)
    try:runner.trip(nav,proposal)
    except BaseException as error:
        runner.journal.update(status='stopped-for-actual-state-review',verified=False)
        runner.record('stop',reason=str(error),error=type(error).__name__);raise


if __name__=='__main__':main()
