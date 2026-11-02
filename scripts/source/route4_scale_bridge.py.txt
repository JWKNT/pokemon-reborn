"""Source-bound Route4 Heart Scale bridge, dry-run unless --execute.

Imports ordinary UI helpers ONLY inside execution methods. No controls,
captures, current planner/native/save or active logs are read in development.
Reuse calcenon queue world/position/page guards, layer_walk, surface_walk,
eventq and the single requested normal checkpoint. Never blind-replay.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from calcenon_agate_queue import Runner as ExistingRunner, event, need, selected_page

ROOT=Path(__file__).resolve().parents[1]
PHASES=('all','dock','board','cross','pickup')
SURF_SPRITES=('boy_surf','girl_surf','boy2_surf','girl2_surf','nb_surf','nb2_surf')


def source_proof():
    anchor,item=event(715,97),event(715,64)
    need((anchor['x'],anchor['y'])==(50,25),'Layer anchor moved')
    p=anchor['pages'][0]
    need(p['trigger']==1 and not any(v for k,v in p['condition'].items() if k.endswith('_valid')),
         'Layer anchor must be unconditional player-touch')
    need([(c['code'],c['parameters']) for c in p['list'] if c['code']!=0]==[(121,[410,410,0])],
         'Layer anchor must have only the source410True setter')
    need((item['x'],item['y'])==(57,20),'Heart Scale event moved')
    need(item['pages'][0]['list'][0]['parameters']==[12,'Kernel.pbItemBall(:HEARTSCALE)'],
         'Pickup must be normal Heart Scale item-ball')
    need(any(c['code']==123 and c['indent']==1 and c['parameters']==['A',0]
             for c in item['pages'][0]['list']),'Pickup self-A must follow success condition')
    return [{'map':715,'event':e['id'],'sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()}
            for e in (anchor,item)]


def preflight(status):
    party=status.get('party',[])
    need(len(party)==6 and party[0]['level']==90,'Frozen six and level90 lead required')
    need(party[0]['hp']==party[0]['totalhp'] and party[0]['status'] is None,
         'Heal lead before the dry approach')
    need(any(p.get('species')=='SWAMPERT' and 'SURF' in {m['move'] for m in p.get('moves',[])}
             for p in party),'Frozen owned Swampert must know Surf')
    bag=status.get('bag',{}).get('contents',{})
    need(bag.get('HEARTSCALE',0)==0,'Already own a Scale: skip this pickup rather than duplicate it')
    need(bag.get('SUPERREPEL',0)>0,'Owned SuperRepel required for this walk')


def proposal(layer=None):
    return {'status':'source proposal, not executed','arrival':[715,65,17],
            'observed_layer_argument':layer,'steps':[
        ['layer_walk',715,50,23,'OBSERVED410' if layer is None else layer,0],
        {'ordinary_keys':['down:.03','c','wait:.7'],'only_choice':'verified Surf Yes/No → Yes',
         'require':'715[50,24] and exact visible installed Surf avatar'},
        {'ordinary_keys':['down:.12','wait:.5'],'require':'715[50,25] genuine overworld/Surf',
         'completed_source_only':'715E97 sets planner410True'},
        ['surface_walk',715,57,21],['eventq',715,64,'item'],
        {'require':'visible Heart Scale acquisition, then one normal checkpoint',
         'checkpoint':'Route4-Scale-129','proof':'postbag HEARTSCALE>=1 and native715,64,A=True'}],
        'source_proof':source_proof(),
        'stop':'Any capture restart/interruption, encounter, wrong coordinate/page/avatar or unknown dialogue. Re-observe and choose a fresh phase; never replay existing journal.'}


class Runner(ExistingRunner):
    def __init__(self,args,binding):
        self.args=args;self.path=args.journal.resolve()
        need(self.path.is_relative_to(ROOT) and not self.path.exists(),
             'Use a new workspace journal after reviewing any partial previous run')
        self.journal={'frozen_status_sha256':binding,'source_proof':source_proof(),
                      'phase':args.phase,'events':[],'pending':None}
        self.write()

    def health(self):
        h=json.loads((ROOT/'recordings/capture-health.json').read_text())
        need(h.get('active') is True and time.time()-h.get('epoch',0)<2,
             'Recording health is not fresh; no input')
        return h

    def run(self,script,*args):
        before=self.health()
        self.journal['pending']={'script':script,'args':list(args),'epoch':time.time()};self.write()
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*map(str,args)],
                              capture_output=True,text=True,check=True)
        print(result.stdout,flush=True)
        after=self.health()
        self.record('ordinary-helper-returned',script=script,args=list(args),stdout=result.stdout)
        # Existing movement helper may recover and replan, but this bridge never
        # proceeds into its next phase on a restarted capture without review.
        need(before.get('pid')==after.get('pid') and
             before.get('restart_count',0)==after.get('restart_count',0),
             'Capture restarted during helper: stop and re-observe actual endpoint')
        self.journal['pending']=None;self.write()
        return result.stdout

    def keys(self,*keys):
        from play import act
        before=self.health()
        self.journal['pending']={'normal_keys':list(keys),'epoch':time.time()};self.write()
        act(*keys)
        after=self.health()
        need(before.get('pid')==after.get('pid') and
             before.get('restart_count',0)==after.get('restart_count',0),
             'Capture restarted during keys; stop without replay')
        self.record('ordinary-keys-returned',keys=list(keys));self.journal['pending']=None;self.write()

    def surf_visible(self):
        from play import snap,NATIVE
        from sprite_sensor import detect
        snap()
        names=(self.args.surf_sprite,) if self.args.surf_sprite else SURF_SPRITES
        matches={name:detect(NATIVE,name,scale=self.args.sprite_scale) for name in names}
        hits=[(name,p) for name,poses in matches.items() for p in poses]
        need(len(hits)==1,'Surf avatar must match one exact installed sprite; inspect public screenshot')
        self.record('public-surf-avatar-confirmed',sprite=hits[0][0],pose=hits[0][1],
                    screenshot=str(NATIVE))

    def dock(self):
        self.position(715,(715,65,17))
        need(self.nav().get('switches',{}).get('410',False)==bool(self.args.layer),
             'Observed layer argument disagrees with completed planner evidence')
        self.run('layer_walk',715,50,23,self.args.layer,0)
        self.position(715,(715,50,23))
        need(self.nav().get('switches',{}).get('410') is False,'Dry dock requires observed410False')

    def board(self):
        from play import read
        self.position(715,(715,50,23))
        need(self.nav().get('switches',{}).get('410') is False,'Board only from verified lower dry dock')
        self.keys('down:.12','c','wait:.7')
        for _ in range(6):
            text=read();compact=re.sub('[^a-z]','',text.lower());self.record('boarding-public-text',text=text)
            need(not re.search(r'\bfight\b|\bhp\b|\bwild\b|pp:',text.lower()),'Encounter interrupted boarding')
            if 'surf' in compact and ('wouldyouliketo' in compact or 'youliketosurf' in compact):
                self.run('choose_dialog','Yes|No','Yes')
            elif 'usedsurf' in compact or 'surf!' in text.lower():
                self.keys('c','wait:1')
            else:
                self.world();break
        else:
            raise ValueError('Surf boarding messages did not resolve')
        self.position(715,(715,50,24));self.surf_visible()
        self.keys('down:.12','wait:.5')
        self.position(715,(715,50,25));self.surf_visible()
        self.active_source(715,97,0)
        self.mirror(715,97,0)
        need(self.nav()['switches']['410'] is True,'Only witnessed E97 completion can establish surf layer')

    def cross(self):
        self.position(715,(715,50,25));self.surf_visible()
        need(self.nav().get('switches',{}).get('410') is True,'Cross requires witnessed E97 layer')
        self.run('surface_walk',715,57,21)
        self.position(715,(715,57,21))

    def pickup(self):
        self.position(715,(715,57,21));self.active_source(715,64,0)
        out=self.run('eventq',715,64,'item')
        compact=re.sub('[^a-z]','',out.lower())
        need('heartscale' in compact and any(w in compact for w in ('obtained','found','put','bag')),
             'Missing visible Heart Scale acquisition: inspect before any checkpoint')
        self.record('visible-heartscale-acquisition',evidence=out)
        self.world();self.run('checkpoint',self.args.checkpoint)
        after=json.loads((ROOT/'notes'/f'{self.args.checkpoint}-status.json').read_text())
        nav=json.loads((ROOT/'notes'/f'{self.args.checkpoint}-navigation.json').read_text())
        need(after.get('map')==715 and after.get('bag',{}).get('contents',{}).get('HEARTSCALE',0)>=1,
             'Post-checkpoint bag did not prove the Scale')
        need(nav.get('self_switches',{}).get('715,64,A') is True,
             'Native checkpoint did not prove successful pickup self-A')
        self.record('heartscale-native-checkpoint-balanced',checkpoint=self.args.checkpoint,
                    scale_count=after['bag']['contents']['HEARTSCALE'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true');p.add_argument('--phase',choices=PHASES,default='all')
    p.add_argument('--from-phase',choices=PHASES[1:],help='Explicit reviewed suffix resume; always use a fresh journal')
    p.add_argument('--layer',type=int,choices=(0,1));p.add_argument('--frozen-status',type=Path)
    p.add_argument('--journal',type=Path,default=ROOT/'work/route4-scale-129-progress.json')
    p.add_argument('--checkpoint',default='Route4-Scale-129')
    p.add_argument('--surf-sprite',choices=SURF_SPRITES);p.add_argument('--sprite-scale',type=int,choices=(1,2,3,4),default=4)
    args=p.parse_args()
    if not args.execute:
        if args.frozen_status:preflight(json.loads(args.frozen_status.read_text()))
        print(json.dumps(proposal(args.layer),indent=2));return
    need(args.frozen_status is not None,'Explicit frozen outside-battle party/bag evidence required')
    path=args.frozen_status.resolve();need(path.is_relative_to(ROOT),'Frozen evidence must be in workspace')
    raw=path.read_bytes();preflight(json.loads(raw))
    need(args.phase not in ('all','dock') or args.layer is not None,'Supply actually observed410 for dry approach')
    need(args.checkpoint.replace('-','').replace('_','').isalnum(),'Unsafe checkpoint label')
    runner=Runner(args,hashlib.sha256(raw).hexdigest())
    try:
        phases = ('dock','board','cross','pickup') if args.phase=='all' else (args.phase,)
        if args.from_phase:
            need(args.phase == 'all', '--from-phase requires the default all phase')
            phases = phases[phases.index(args.from_phase):]
        for phase in phases:
            getattr(runner,phase)();runner.record('phase-completed',phase=phase)
    except BaseException as error:
        runner.record('stopped-requires-actual-state-review',error=str(error),pending=runner.journal['pending'])
        raise


if __name__=='__main__':main()
