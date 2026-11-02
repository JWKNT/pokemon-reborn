"""Normal initial-state Hardy tuner queue; source-only unless --execute.

No UI, save, current planner/native or logs are inspected by import/default run.
Execution requires an explicit fresh normal checkpoint after all three trainers,
actual public player/tuner pixels, and a new journal. No blind mid-puzzle replay.
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
from calcenon_agate_queue import Runner as Base, event, need

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Applications/Reborn.app/Contents/Game')
TARGETS=(3,5,7,2,2,0,1,1)
YS=(45,41,37,33,22,18,14,10)
TRAINERS=(22,35,36)
PLAYER_SPRITES=('boy_walk','boy_run')


def source_proof():
    assets=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/hardy_piano_source.rb')],
                                            stderr=subprocess.DEVNULL))
    need((assets['width'],assets['height'],assets['tileset_name'])==(25,60,'Agate Gym'),
         'Installed tuner hall/tileset changed')
    need(assets['door_base_tiles']==[479,573,594], 'Installed closed-door overlay changed')
    proof=[]
    for i,(y,note) in enumerate(zip(YS,TARGETS)):
        e=event(739,23+i);p=e['pages'][0];var=441+i
        need((e['x'],e['y'])==(14,y) and len(e['pages'])==1,
             'Installed initial tuner geometry changed')
        need(p['trigger']==0 and p['graphic']['tile_id']==604 and
             not p['graphic']['character_name'] and not p['through'],
             'Tuner must remain ordinary blocked tile604 action event')
        cs=p['list']
        need([c['parameters'] for c in cs if c['code']==122]==
             [[var,var,0,6,0,0],[var,var,2,0,14]],'Tuner value is not actual event x minus14')
        need([c['parameters'] for c in cs if c['code']==355]==
             [['pbPushThisObject'],['pbPushThisObject']], 'Unknown tuner script')
        need(not any(c['code'] in [101,102,201,301] for c in cs), 'Unexpected tuner dialogue/choice/battle')
        proof.append({'event':23+i,'initial':[14,y],'target':[14+note,y],
                      'variable':var,'value':note,'sha256':hashlib.sha256(json.dumps(e,sort_keys=True).encode()).hexdigest()})
    climb=event(739,1)['pages'][0]['list']
    need([c['parameters'] for c in climb[404:412]]==
         [[1,441+i,0,v,0] for i,v in enumerate(TARGETS)], 'Installed eight-note solution changed')
    need(climb[416]['parameters']==[1022,1022,0], 'Installed solution door flag changed')
    dx=dy=0
    for c in climb:
        if c['code']!=209:continue
        for m in c['parameters'][1]['list']:
            mx,my={1:(0,1),2:(-1,0),3:(1,0),4:(0,-1)}.get(m['code'],(0,0))
            if m['code']==14:mx,my=m['parameters']
            dx+=mx;dy+=my
    need((dx,dy)==(0,-38),'Installed climb landing changed')
    for eid in TRAINERS:
        e=event(739,eid)
        need(e['pages'][0]['trigger']==2 and
             any(c['code']==123 and c['parameters']==['A',0] and c['indent']==1
                 for c in e['pages'][0]['list']), 'Trainer completion source changed')
    door=event(739,31)['pages'][0]
    need(door['condition']['switch2_valid'] and door['condition']['switch2_id']==1022 and
         door['graphic']['tile_id']==573 and
         [c['parameters'] for c in door['list'] if c['code']==201]==[[0,740,9,21,0,1]],
         'Open door source changed')
    src=(GAME/'Scripts/Field.rb').read_text()
    need('event.move_direction(direction)' in src and 'pbPushThisEvent("strengthrock", direction)' in src,
         'Installed push semantics changed')
    return {'assets':assets,'tuners':proof,'climb':[739,5,46,5,8],'open_door':[739,11,4,740,9,21],
            'stop':'740[9,21], before Hardy player-touch740[9,18]'}


def preflight(status,nav,*,now=None,start_tuner=0):
    need(type(start_tuner) is int and 0<=start_tuner<=7,'Explicit next tuner index0..7 required')
    need(status.get('map')==739,'Fresh checkpoint must be in the tuner hall739')
    saved=datetime.fromisoformat(status['save_mtime']).timestamp()
    if now is not None:need(-5<=now-saved<=120,'Checkpoint must be freshly written, at most120s old')
    party=status.get('party',[])
    need(len(party)==6 and any('ROCKCLIMB' in {m['move'] for m in p.get('moves',[])} for p in party),
         'Six-member party with an owned RockClimb user required')
    need(nav.get('switches',{}).get('1022',False) is False,'Already-open puzzle is not the initial case')
    need(nav.get('variables',{}).get('391',0)<61,'Hardy is already completed')
    for eid in TRAINERS:
        need(nav.get('self_switches',{}).get(f'739,{eid},A') is True,
             f'Trainer739E{eid} must be actually defeated before this queue')
    for i,y in enumerate(YS):
        expected_x=14+TARGETS[i] if i<start_tuner else 14
        need(nav.get('positions',{}).get('739',{}).get(str(23+i))==[expected_x,y],
             'Completed tuners must match targets; every remaining tuner must be initial')
        if i<start_tuner:
            need(nav.get('variables',{}).get(str(441+i))==TARGETS[i],
                 'Fresh saved completed tuner value differs from its target')


def group_keys(count):
    need(isinstance(count,int) and 0<count<=7,'Only source-bounded positive tuner groups')
    # The push moves only the tuner. Follow into its vacated square after each
    # C so the next interaction remains adjacent; never hold C or movement.
    return tuple(k for _ in range(count) for k in
                 ('c:.12','wait:.45','right:.12','wait:.2'))


def tile_asset(tile_id):
    from PIL import Image
    need(tile_id in [573,604],'Only reviewed tuner/open-door tiles')
    x=(tile_id-384)%8*32;y=(tile_id-384)//8*32
    return Image.open(GAME/'Graphics/Tilesets/Agate Gym.png').convert('RGBA').crop((x,y,x+32,y+32))


def tile_score(image,template,player_foot,player_xy,tile_xy,scale):
    """Pure exact source tile pixels at an actual player-relative map square."""
    from PIL import Image
    need(scale in [1,2,3,4],'Unreviewed tile scale')
    px,py=player_foot;x,y=player_xy;tx,ty=tile_xy
    left=round(px+(tx-x)*32*scale-16*scale)
    top=round(py+(ty-y)*32*scale-32*scale)
    side=32*scale
    need(0<=left and 0<=top and left+side<=image.width and top+side<=image.height,
         'Expected source tile is outside the actual public frame')
    target=template.resize((side,side),Image.Resampling.NEAREST)
    crop=image.crop((left,top,left+side,top+side)).convert('RGB')
    pairs=[(p,q) for p,q in zip(crop.getdata(),target.getdata()) if q[3]>250]
    need(len(pairs)>=500*scale*scale,'Reviewed source tile has insufficient opaque proof')
    score=sum(max(abs(p[i]-q[i]) for i in range(3))<=3 for p,q in pairs)/len(pairs)
    need(score>=.97,'Actual tuner/door source tile mismatch; no position/effect credited')
    return {'score':score,'rect':[left,top,left+side,top+side]}


class Runner(Base):
    def __init__(self,args,status_binding,nav_binding):
        self.args=args;self.path=args.journal.resolve()
        need(self.path.is_relative_to(ROOT) and not self.path.exists(),'A NEW workspace journal is required; no replay')
        self.work=ROOT/'work'/self.path.stem
        need(not self.work.exists(),'Evidence directory exists; review instead of replay')
        self.work.mkdir()
        self.journal={'frozen_status_sha256':status_binding,'frozen_navigation_sha256':nav_binding,
                      'source_proof':source_proof(),'start_tuner':args.start_tuner,'events':[],'pending':None}
        self.write()

    def health(self):
        h=json.loads((ROOT/'recordings/capture-health.json').read_text())
        need(h.get('active') is True and time.time()-h.get('epoch',0)<2,'Recording is not fresh; no input')
        return h

    def same_capture(self,a,b):
        need(a.get('pid')==b.get('pid') and a.get('restart_count',0)==b.get('restart_count',0),
             'Capture restarted; stop and review actual endpoint, never replay')

    def keys(self,*keys):
        from play import act
        before=self.health();self.journal['pending']={'keys':list(keys),'epoch':time.time()};self.write()
        act(*keys);self.same_capture(before,self.health())
        self.record('ordinary-keys-returned',keys=list(keys));self.journal['pending']=None;self.write()

    def run(self,script,*args):
        serialized_args=list(map(str,args))
        before=self.health();self.journal['pending']={'script':script,'args':serialized_args,'epoch':time.time()};self.write()
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*serialized_args],
                              check=True,capture_output=True,text=True)
        print(result.stdout,flush=True);self.same_capture(before,self.health())
        self.record('ordinary-helper-returned',script=script,args=serialized_args,stdout=result.stdout)
        self.journal['pending']=None;self.write();return result.stdout

    def pixels(self,player_xy,*,tile_id=None,tile_xy=None,facing=None):
        from play import snap,NATIVE
        from sprite_sensor import detect
        from PIL import Image,ImageCms
        import io
        self.health();snap();native=Image.open(NATIVE);image=native.convert('RGB')
        need(native.size==(2272,1816) if self.args.sprite_scale==4 else True,
             'Expected calibrated shadowed retina frame; review scale')
        if native.info.get('icc_profile'):
            image=ImageCms.profileToProfile(image,ImageCms.ImageCmsProfile(io.BytesIO(native.info['icc_profile'])),
                                           ImageCms.createProfile('sRGB'),outputMode='RGB')
        seen=[(name,pose) for name in PLAYER_SPRITES for pose in detect(NATIVE,name,scale=self.args.sprite_scale)]
        need(len(seen)==1,'Actual installed player sprite is not unique; stop for visual review')
        name,pose=seen[0]
        if facing is not None:need(pose['pose'][0]==facing,'Actual rendered player facing differs')
        proof=tile_score(image,tile_asset(tile_id),pose['foot'],player_xy,tile_xy,self.args.sprite_scale) if tile_id else None
        path=self.work/f'public-{len(self.journal["events"])}.png';native.save(path)
        self.record('public-rendered-pixels',image=str(path),player_xy=list(player_xy),sprite=name,
                    player_pose=pose,tile_id=tile_id,tile_xy=list(tile_xy) if tile_xy else None,tile_proof=proof)

    def walk(self,x,y):
        actual=self.position(739)
        path=self.work/'route-next.json';path.write_text(json.dumps([[739,actual[1],actual[2],x,y,[]]]))
        self.run('queue_route',path,'--from-verified')
        self.position(739,(739,x,y))

    def facing(self,xy,direction,pose):
        self.keys(direction+':.03','wait:.3')
        self.position(739,(739,*xy));self.pixels(xy,facing=pose)

    def mirror_tuner(self,eid,xy,var,value):
        # Planner notes only, after observed coordinates and source tile pixels.
        state=self.nav();state.setdefault('positions',{}).setdefault('739',{})[str(eid)]=list(xy)
        state.setdefault('variables',{})[str(var)]=value
        (ROOT/'notes/navigation-state.json').write_text(json.dumps(state)+'\n')
        self.record('witnessed-tuner-effects-mirrored-to-planner',event=eid,position=list(xy),variable=var,value=value)

    def solve(self):
        self.position(739);self.no_auto_battle(739)
        for i,(y,count) in enumerate(zip(YS,TARGETS)):
            if i<self.args.start_tuner:continue
            eid=23+i;self.active_source(739,eid,0)
            need(self.nav()['positions']['739'][str(eid)]==[14,y],'Planner tuner no longer initial; stop')
            if count:
                self.walk(13,y);self.facing((13,y),'right',2)
                self.pixels((13,y),tile_id=604,tile_xy=(14,y),facing=2)
                self.keys(*group_keys(count))
                player=(13+count,y);tuner=(14+count,y)
                self.position(739,(739,*player));self.pixels(player,tile_id=604,tile_xy=tuner,facing=2)
            else:
                # Vertical interaction explicitly refreshes x−14=0 without a push.
                # Stand above: the player's tall sprite otherwise occludes the
                # bottom of the source tile when inspecting from below.
                self.walk(14,y-1);self.facing((14,y-1),'down',0)
                self.pixels((14,y-1),tile_id=604,tile_xy=(14,y),facing=0)
                self.keys('c:.12','wait:.6')
                self.position(739,(739,14,y-1));self.pixels((14,y-1),tile_id=604,tile_xy=(14,y),facing=0)
                tuner=(14,y)
            self.mirror_tuner(eid,tuner,441+i,count)
        self.record('all-eight-tuners-verified',values=list(TARGETS))

    def climb_and_enter(self):
        from play import read
        need([self.nav()['variables'][str(441+i)] for i in range(8)]==list(TARGETS),'Unproved eight-note values')
        self.walk(5,46);self.facing((5,46),'up',3)
        self.keys('c:.12','wait:1')
        text=read();compact=re.sub('[^a-z]','',text.lower())
        need(not re.search(r'\bfight\b|\bhp\b|\bpp:',text.lower()),'Unexpected battle during climb')
        if 'rockclimb' in compact:
            need('usedrockclimb' in compact,'RockClimb prerequisite/message requires review; no extra C')
            self.keys('c:.12','wait:1')
        else:self.world()
        self.keys('wait:12')
        self.position(739,(739,5,8));self.record('actual-forced-climb-landing',position=[739,5,8])
        self.walk(11,6)
        self.pixels((11,6),tile_id=573,tile_xy=(11,4))
        state=self.nav();state.setdefault('switches',{})['1022']=True
        (ROOT/'notes/navigation-state.json').write_text(json.dumps(state)+'\n')
        self.record('actual-open-door-proved-planner1022',source='739E1 exact note branch + actual open-door tile573')
        self.active_source(739,31,0);self.run('eventq',739,31,'enter')
        self.position(740,(740,9,21))
        self.record('complete-stopped-before-Hardy',position=[740,9,21],forbidden_trigger=[740,9,18])
        self.journal['complete']=True;self.write()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true');p.add_argument('--frozen-status',type=Path)
    p.add_argument('--frozen-navigation',type=Path);p.add_argument('--journal',type=Path)
    p.add_argument('--sprite-scale',type=int,choices=(1,2,3,4),default=4)
    p.add_argument('--start-tuner',type=int,choices=range(8),default=0,
                   help='Reviewed next tuner index; earlier tuners require exact fresh saved targets/values')
    args=p.parse_args();proof=source_proof()
    if not args.execute:
        print(json.dumps({'status':'source-only; no UI inspected or input sent',**proof},indent=2));return
    need(args.frozen_status and args.frozen_navigation and args.journal,
         '--execute requires explicit fresh frozen status/navigation and a new journal')
    paths=[path.resolve() for path in [args.frozen_status,args.frozen_navigation]]
    need(all(path.is_relative_to(ROOT) for path in paths),'Frozen evidence must be in workspace')
    raw=[path.read_bytes() for path in paths];status,nav=map(json.loads,raw)
    preflight(status,nav,now=time.time(),start_tuner=args.start_tuner)
    actual=json.loads((ROOT/'notes/navigation-state.json').read_text())
    preflight(status,actual,now=time.time(),start_tuner=args.start_tuner)
    need(actual['positions']['739']==nav['positions']['739'],'Planner differs from fresh checkpoint positions')
    runner=Runner(args,*[hashlib.sha256(b).hexdigest() for b in raw])
    try:runner.solve();runner.climb_and_enter()
    except BaseException as error:
        runner.record('stopped-requires-actual-review',error=str(error),pending=runner.journal['pending']);raise


if __name__=='__main__':main()
