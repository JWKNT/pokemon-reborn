"""Enter an inspected ordinary trainer fight; import/source dry-run sends no input.

Default CLI retains the existing normal UI workflow and fresh intro guards.
--paired-event binds two distinct same-map ordinary trainer sources before the
combined name is accepted. Both sources remain choice-free.
"""
from __future__ import annotations
import argparse
import difflib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]


def trainer_calls(commands):
 text=' '.join(str(c['parameters']) for c in commands)
 return re.findall(r'pbTrainerBattle\(\s*:([A-Za-z0-9_]+)\s*,\s*["\']([^"\']+)["\']',text)


def validate_pair(primary,paired,event,paired_event,trainer_class,name):
 assert type(event)is int and type(paired_event)is int and event!=paired_event and paired_event>0, 'Distinct same-map paired event required'
 names=name.split(' & ')
 assert len(names)==2 and all(names) and len(set(names))==2, 'Paired trainer name must contain two distinct names separated by &'
 first=trainer_calls(primary);second=trainer_calls(paired)
 assert first==[(trainer_class,names[0])] and len(second)==1 and second[0][1]==names[1], 'Paired source trainer declarations do not match both names/order'
 assert not any(c['code']in[102,103,104]for c in primary+paired), 'Paired trainer sources must both be choice-free'
 return {'primary':list(first[0]),'paired':list(second[0]),'events':[event,paired_event],
         'same_map':True,'choice_free':True,'combined_name':name}


def installed_event(mid,eid):
 return json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(mid),str(eid)],stderr=subprocess.DEVNULL))


def dry_source(args):
 # This path reads installed map assets only, never route_map or native state.
 e=installed_event(args.map,args.event);pi=args.source_page if args.source_page is not None else 0
 cs=e['pages'][pi]['list'];result={'source_only':True,'map':args.map,'event':args.event,'page':pi,'no_UI_or_runtime_reads':True}
 if args.paired_event is not None:
  other=installed_event(args.map,args.paired_event);paired=other['pages'][0]['list']
  result['pair']=validate_pair(cs,paired,args.event,args.paired_event,args.trainer_class,args.name)
  cs=list(cs)+list(paired)
 else:
  script=' '.join(str(c['parameters'])for c in cs)
  assert any(k in script for k in ['pbTrainerBattle','pbDoubleTrainerBattle']) and args.trainer_class in script and all(n in script for n in args.name.split(' & '))
  assert not any(c['code']in[102,103,104]for c in cs),'Source dryrun requires directly choice-free event pages'
 return result


def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument('--paired-event',type=int,help='Second same-map ordinary trainer event; both reviewed sources are required');p.add_argument('--dry-run',action='store_true',help='Installed-source validation only; no game/UI/runtime reads');p.add_argument('map',type=int);p.add_argument('event',type=int);p.add_argument('trainer_class');p.add_argument('name');p.add_argument('--expand-common',action='store_true',help='Read inspected common event lists referenced by this event');p.add_argument('--source-page',type=int,help='Explicit inspected page for an already observed autorun dialogue');p.add_argument('--active-dialogue',action='store_true');p.add_argument('--past-choice',action='store_true');p.add_argument('--post-battle-choices',action='store_true');p.add_argument('--reviewed-choice-labels',type=json.loads);p.add_argument('--log-scripted-bgm',action='store_true');p.add_argument('--resume-intro',action='store_true');p.add_argument('--burst-dialogue',action='store_true');p.add_argument('--intro-cycles',type=int,default=160);a=p.parse_args(argv)
 assert 160<=a.intro_cycles<=800
 def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
 if a.dry_run:
  source=dry_source(a)
  print(json.dumps(source,indent=2));return
 import play
 from PIL import Image
 STATE=play.STATE;act=play.act;read=play.read;snap=play.snap
 if a.source_page is not None:
  assert a.active_dialogue,'Explicit page only valid during observed dialogue'
  e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(a.map),str(a.event)],stderr=subprocess.DEVNULL))
  cs=e['pages'][a.source_page]['list']
 else:
  v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(a.map),'0','0'],stderr=subprocess.DEVNULL))
  cs=v['events'][str(a.event)]['list']
 if a.paired_event is not None:
  paired=v['events'][str(a.paired_event)]
  validate_pair(cs,paired['list'],a.event,a.paired_event,a.trainer_class,a.name)
  cs=list(cs)+list(paired['list'])
 if a.expand_common:
  seen=set();pending=list(cs)
  while pending:
   c=pending.pop(0)
   if c['code']!=117 or c['parameters'][0] in seen:continue
   eid=c['parameters'][0];seen.add(eid)
   src="v=load_rgss('/Applications/Reborn.app/Contents/Game/Data/CommonEvents.rxdata');puts JSON.generate(plain(v[ARGV[0].to_i]))"
   common=json.loads(subprocess.check_output(['ruby','-r',str(ROOT/'scripts/read_rgss.rb'),'-e',src,str(eid)],stderr=subprocess.DEVNULL))['list']
   cs.extend(common);pending.extend(common)
 scripts=' '.join(str(c['parameters']) for c in cs)
 assert any(k in scripts for k in ['pbTrainerBattle','pbDoubleTrainerBattle']) and a.trainer_class in scripts and all(n in scripts for n in a.name.split(' & '))
 if a.post_battle_choices:
  battle_index=next(i for i,c in enumerate(cs) if any(k in str(c['parameters']) for k in ['pbTrainerBattle','pbDoubleTrainerBattle']))
  assert all(i>battle_index and c['parameters'][0]==['Yes','No'] for i,c in enumerate(cs) if c['code']==102)
  assert not any(c['code']in[103,104]for c in cs)
 elif a.past_choice:
  assert a.active_dialogue and [c['parameters'][0]for c in cs if c['code']==102]==[a.reviewed_choice_labels or ['Yes','No']]
  assert not any(c['code']in[103,104]for c in cs)
 else:assert not any(c['code'] in [102,103,104]for c in cs),'Choice requires manual review'
 if a.resume_intro:
  prior=json.loads((ROOT/'work/active-trainer-music.json').read_text())
  assert a.active_dialogue and prior['class']==a.trainer_class and prior['name']==a.name
 else:run('trainer_music','start',a.trainer_class,a.name,'--map',a.map)
 if not a.active_dialogue:
  rc=subprocess.call([sys.executable,str(ROOT/'scripts/eventq.py'),str(a.map),str(a.event),'talk'])
  if rc:
   first=[]
   for c in cs:
    if c['code']==101:
     if first:break
     first=[str(c['parameters'][0])]
    elif c['code']==401 and first:first.append(str(c['parameters'][0]))
   text=read();norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
   ellipsis_box=False
   if first and all(z.strip()=='.'*3 for z in first):
    im=Image.open(STATE).convert('RGB');ww,hh=im.size;patch=im.crop((int(ww*.08),int(hh*.75),int(ww*.90),int(hh*.87)))
    ellipse_white=sum(min(z)>235 and max(z)-min(z)<5 for z in patch.getdata())/(patch.width*patch.height)>.75
    bottom=[v['text'] for v in snap() if v['y']>.73 and len(v['text'])>5]
    ellipsis_box=ellipse_white and not bottom and not re.search(r'\bhp\b|fight|yes|no',text,re.I)
   assert rc==2 and first and (ellipsis_box or difflib.SequenceMatcher(None,norm(text),norm(' '.join(first))).ratio()>.65),'Approach interruption needs review'
   print('REVIEWED TRAINER TOUCH DIALOGUE REACHED',flush=True)
 intro=False
 bgm_anchors=[];bgm_seen=set()
 if a.log_scripted_bgm:
  for i,c in enumerate(cs):
   if c['code'] not in [241,242]:continue
   block=[]
   for z in cs[i+1:]:
    if z['code']==101:
     if block:break
     block=[str(z['parameters'][0])]
    elif z['code']==401 and block:block.append(str(z['parameters'][0]))
   if block:bgm_anchors.append((i,' '.join(block),c['parameters'][0]['name'] if c['code']==241 else '__silence__'))
 blocks=[]
 for i,c in enumerate(cs):
  if c['code']==101:blocks.append([i,str(c['parameters'][0])])
  elif c['code']==401 and blocks:blocks[-1][1]+=' '+str(c['parameters'][0])
 battle_boundary=next(i for i,c in enumerate(cs) if any(k in str(c['parameters']) for k in ['pbTrainerBattle','pbDoubleTrainerBattle']))
 for _ in range(a.intro_cycles):
  t=read();print(t,flush=True);low=t.lower();compact=re.sub('[^a-z]','',low)
  if bgm_anchors:
   norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
   for idx,line,track in bgm_anchors:
    if idx not in bgm_seen and difflib.SequenceMatcher(None,norm(t),norm(line)).ratio()>.72:
     with (ROOT/'recordings/music-events.jsonl').open('a')as f:f.write(json.dumps({'epoch':time.time(),'bgm':{'name':track},'source':'inspected-scripted-BGM','map':a.map,'event':a.event,'command_index':idx,'evidence':t})+'\n')
     bgm_seen.add(idx);print('SCRIPTED BGM',track,flush=True)
  # Terra's scripted Blank.ttf removes all text except baked command buttons.
  if (a.map,a.event,a.trainer_class,a.name)==(778,49,'TERRA','T3RR4') and re.search(r'(?<![a-z])hp(?![a-z])',low):
   print('FONTLESS HUD APPEARED: stop for manual review before commands',flush=True);break
  if re.search('[wmuv]ouldliketobattle',compact) or re.search(r'\bvs\b',low):intro=True
  if re.sub('[^a-z]','',a.name.lower()) in compact and 'sentout' in compact:
   intro=True # Public trainer send-out is also an unambiguous intro anchor.
  # The partnered VS card renders names without the literal letters "VS".
  # Require both its allied Aster name and the exact reviewed opposing names.
  card_lines=[re.sub('[^a-z]','',z.lower()) for z in t.splitlines()]
  if '&' in a.name and re.sub('[^a-z]','',a.name.lower()) in card_lines and any(z.startswith('aster') and len(z)>5 for z in card_lines):intro=True
  grid=sum(n in low for n in ['extreme speed','crunch','flanethrouer','flamethrower','morning sun','horning sun','trick room','destiny bond','waterfall','earthquake','light screen','discharge','freeze-dry','freeze-d','ice beam','ice bean','recover','recouer','high jump kick','wide guard','fake out','u-turn','signal beam'])>=2
  if intro and (grid or re.search(r'pp.?\s*\d+',low) or ('fight' in low and 'bag' in low)):
   if grid or re.search(r'pp.?\s*\d+',low):act('x','wait:.5');t=read();assert 'fight' in t.lower() or 'what will' in t.lower()
   print('FIRST BATTLE COMMAND READY',flush=True);break
  if not intro and (grid or re.search(r'pp[:.]?\s*\d+',low)):
   raise SystemExit('Unobserved intro at move grid requires review; no battle move selected')
  if ('fight' in low or 'what will' in low) and re.search(r'(?<![a-z])f?hp(?![a-z])',low):
   assert intro,'Unobserved intro requires review'
   print('FIRST BATTLE COMMAND READY',flush=True);break
  if any(z.strip().lower()in['yes','no']for z in t.splitlines()) or 'choose a pok' in low:raise SystemExit('Unexpected intro state')
  im=Image.open(STATE).convert('RGB');w,h=im.size;box=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
  white=sum(min(z)>235 and max(z)-min(z)<5 for z in box.getdata())/(box.width*box.height)
  def darkrow(y):
   px=[im.getpixel((x,int(h*y)))for x in range(int(w*.08),int(w*.90))]
   return sum(max(z)<95 for z in px)/len(px)
  bordered= max(darkrow(y)for y in [.721,.725,.729,.733])>.80 and max(darkrow(y)for y in [.895,.900,.905,.910])>.80
  textbox=white>.55 or (white>.35 and bordered)
  # Ellipsis-only lines can be completely absent from OCR. The visible white
  # dialogue box is sufficient after the event's choice-free source review.
  if textbox:
   presses=1
   if a.burst_dialogue and not intro and not re.search(r'(?<![a-z])f?hp(?![a-z])|sent.?out|go!',low) and not any(c['code']in[102,103,104]for c in cs[:battle_boundary]):
    # Only pre-battle choices constrain this intro. Post-victory choices cannot
    # be reached because public intro/command guards stop this driver first.
    # Large, source-reviewed Terra shouts may yield no OCR. Two short presses
    # reveal/advance those boxes; observed battle intros remain single-step.
    presses=2
    normburst=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
    matches=[(difflib.SequenceMatcher(None,normburst(t),normburst(b)).ratio(),i)for i,(_,b)in enumerate(blocks)]
    if matches and len(normburst(t))>12:
     score,idx=max(matches)
     before=[j for j,(command,_)in enumerate(blocks)if command<battle_boundary]
     if score>.70 and idx in before and max(before)-idx>12:
      presses=5
      for command,_,_ in bgm_anchors:
       anchor=next((j for j,(start,_)in enumerate(blocks)if start>command),len(blocks))
       if abs(anchor-idx)<=8:presses=1
     elif score>.70:presses=1
   act(*sum((['c','wait:.15' if a.burst_dialogue and not intro else 'wait:.35']for _ in range(presses)),[]))
  else:act('wait:.5')
 else:raise SystemExit('Intro limit')


if __name__=="__main__":main()
