"""Bounded UI battle policy: fixed actor/move, approved foes, stop at switches."""
from play import *
from learning import resolve
import argparse,re,difflib
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('actor');p.add_argument('slot',type=int);p.add_argument('--foes',required=True);p.add_argument('--wild',action='store_true');p.add_argument('--double',action='store_true');p.add_argument('--spread',action='store_true',help='Keep double HUD checks but do not open an individual target for a spread move');p.add_argument('--hp-lower',action='store_true');p.add_argument('--target',type=int,default=1,choices=[1,3]);p.add_argument('--turns',type=int,default=16);p.add_argument('--stay',action='store_true');p.add_argument('--stay-team-reviewed',action='store_true',help='Stay for every member of a fully inspected trainer team');p.add_argument('--watch',action='store_true');p.add_argument('--policy');p.add_argument('--foe-slots');p.add_argument('--min-hp',type=float,default=0);p.add_argument('--recover-below',type=float,default=0);p.add_argument('--recover-slot',type=int,default=2);p.add_argument('--heal-below',type=float,default=0);p.add_argument('--heal-item',default='Super Potion');p.add_argument('--status-move',action='store_true',help='Reviewed non-damaging move may continue through Destiny Bond messages');p.add_argument('--stop-foes',default='');p.add_argument('--stop-allies',default='');p.add_argument('--cure-sleep',action='store_true',help='Bounded Full Heal on actual own SLP HUD before attack');p.add_argument('--stop-after-victory',action='store_true');p.add_argument('--stop-after-battle',action='store_true');p.add_argument('--auto-misty',action='store_true',help='Sylveon casts Misty only when the public backdrop is Inverse');p.add_argument('--require-field',choices=['misty','inverse'],help='Stop before any turn if the rendered field differs');p.add_argument('--stop-phrase',default='');p.add_argument('--world-pause',action='store_true');p.add_argument('--openers');a=p.parse_args();default_hp_lower=a.hp_lower;foe_slots=json.loads(a.foe_slots) if a.foe_slots else None;policy=json.loads(pathlib.Path(a.policy).read_text()) if a.policy else None
openers=json.loads(a.openers) if a.openers else {};opened=set()
assert not openers or foe_slots, 'Opening move requires a per-foe normal move policy'
foes=a.foes.lower().split(',');turns=0;blank=0;won=False;heals=0;cures=0;recovery_before=None;missing_hud=0
stop_foes=a.stop_foes.lower().split(',') if a.stop_foes else []
if a.policy and policy and '_stop_foes' in policy:
 stop_foes=policy.pop('_stop_foes')
stop_moves=[]
control=ROOT/'notes/battle-control.json';approved_switch=False
for _ in range(100):
 if control.exists():
  override=json.loads(control.read_text())
  if override.get('stop'):print('STOP REQUESTED',flush=True);break
  if 'target' in override:a.target=int(override['target'])
  if 'slot' in override:a.slot=int(override['slot'])
  if 'heal_below' in override:a.heal_below=float(override['heal_below'])
  if 'heal_item' in override:a.heal_item=override['heal_item']
  if 'stop_moves' in override:stop_moves=override['stop_moves']
 r=snap();t=' '.join(v['text'] for v in r);low=t.lower();print(t,flush=True)
 has_hud=bool(re.search(r'(?<![a-z])f?hp(?![a-z])',low)) or any(.40<v['y']<.72 and re.sub('[^a-z]','',a.actor.lower()) in re.sub('[^a-z]','',v['text'].lower()) for v in r)

 # Stop a victory-boundary policy if a fast card passed between OCR samples.
 # The caller must review the scene; never auto-advance its dialogue.
 missing_hud=missing_hud+1 if turns>0 and not has_hud else 0
 if a.stop_after_victory and missing_hud>=2:
  print('COMBAT HUD CLEARED — review public victory boundary',flush=True);break
 compact_move=re.sub('[^a-z]','',low)
 if 'foe' in low and any('used'+re.sub('[^a-z]','',m.lower()) in compact_move for m in stop_moves):
  print('REVIEWED SETUP MOVE STOP',flush=True);break
 if any(w in low for w in ['close bag','is selected','tmx1 cut','medicine','sort a:']):print('BAG REVIEW',flush=True);break
 if any(v['text'].strip().lower() in ['sirius','doctor','go upstairs','stay downstairs'] for v in r):print('STORY CHOICE REVIEW',flush=True);break
 if not a.status_move and (('destiny bond' in low and 'used' in low) or 'trying to take its foe down' in low):print('DESTINY BOND REVIEW',flush=True);break
 if not a.status_move and any(w in low for w in ["doesn't affect", 'does not affect']):print('MOVE IMMUNITY REVIEW',flush=True);break
 if a.stop_phrase and a.stop_phrase.lower() in low:print('DIALOGUE STOP',flush=True);break
 if 'out of usable' in low:print('LOSS REVIEW',flush=True);break
 if 'hid behind a rock' in low:print('ROCKY FIELD IMMUNITY REVIEW',flush=True);break
 if 'for winning' in low or re.search(r'de.?feated',low):
  won=True
  if a.stop_after_victory:print('VICTORY ANCHOR',flush=True);break
 if won and a.stop_after_battle and not has_hud:print('VICTORY HUD CLEARED',flush=True);break
 if won and not has_hud and not a.world_pause:
  imdone=Image.open(STATE).convert('RGB');ww,hh=imdone.size;patch=imdone.crop((int(ww*.08),int(hh*.75),int(ww*.90),int(hh*.87)))
  if sum(min(px)>210 for px in patch.getdata())/(patch.width*patch.height)<.45:
   print('VICTORY OVERWORLD OR TRANSITION',flush=True);break
 if 'send in' in low or 'sendin' in low:
  incoming=re.split(r'send\s*in',low,maxsplit=1)[-1]
  if any(difflib.SequenceMatcher(None,n,w.strip('.,')).ratio()>=.78 for n in stop_foes for w in incoming.split()):
   print('REVIEWED INCOMING FOE STOP',incoming,flush=True);break
  approved_switch=any(difflib.SequenceMatcher(None,n,w.strip('.,')).ratio()>=.78 for n in foes for w in incoming.split())
 if turns>=a.turns and ('change pok' in low or 'switch your' in low):
  print('TURN BUDGET SWITCH REVIEW',flush=True);break
 if ((a.stay and approved_switch) or a.stay_team_reviewed) and ('change pok' in low or 'switch your' in low):
  act('x','wait:1.2');approved_switch=False;continue
 if ('cancel' in low and low.count('hp')>=5) or 'switch in' in low or 'no energy left' in low:break
 if any(k in low for k in ['choose a pok','change pok','switch your','no pp','disabled']) or re.search(r'\b(?:yes|tes)\b',low):break
 if re.search(r'\ble[vw]el\s*\d+\s*[!i]',low) or 'max. hp' in low or 'max.hp' in low:
  act('c','wait:0.5');continue
 if 'trying to learn' in low:
  if not resolve(t):break
  continue
 if ('what will' not in low and sum(n in low for n in ['high jump kick','high jump klick','hlide guard','lide guard','hide guard','wide guard','fake üut','fake out','u-turn','extreme speed','crunch','flanethrouer','flamethrower','morning sun'])>=2) or 'pp:' in low or re.search(r'pp.?\s*\d+[/0]\d+',low) or (re.search(r'\d+\s*[,/]\s*[,/]?\s*\d+',low) and 'what will' not in low and any(m in low for m in ['night slash','might slash','rock smash','rock snash','flanethrouer','ice bean'])):
  act('x','wait:0.4');continue
 if re.search(r'\bfight\b',low) and re.search(r'(?<![a-z])f?hp(?![a-z])',low):
  enemy=' '.join(v['text'].lower().translate(str.maketrans({'р':'p','у':'y','а':'a','о':'o','с':'c','е':'e','х':'x','к':'k','і':'i','ј':'j'})) for v in r if v['y']<.37).replace('klink lang','klinklang').replace('meougtic','meowstic').replace('meoustic','meowstic').replace('jumplutt','jumpluff').replace('nin jask','ninjask')
  own=' '.join(v['text'].lower() for v in r if v['x']>.5 and .40<v['y']<.71).replace('klink lang','klinklang').translate(str.maketrans({'р':'p','у':'y','а':'a','о':'o','с':'c','е':'e','х':'x','п':'n'}))
  # Animated HUD names can be partly covered; the command prompt independently
  # names the active Pokémon whose action is being chosen.
  own+=' '+' '.join(v['text'].lower() for v in r if v['y']>.72 and v['x']<.5)
  if re.search(r'\b(?:frz|par)',own):print('FROZEN OR PARALYZED ACTOR REVIEW; no further move selected',own,flush=True);break
  if a.stop_allies and any(any(difflib.SequenceMatcher(None,n,w.strip('.,')).ratio()>=.78 for w in own.split()) for n in a.stop_allies.lower().split(',')):print('REVIEWED ALLY STOP',own,flush=True);break
  if any(any(difflib.SequenceMatcher(None,n.lower(),w.strip('.,')).ratio()>=.78 for w in enemy.split()) for n in stop_foes):print('REVIEWED FOE STOP',enemy,flush=True);break
  if policy:
   prompt=' '.join(v['text'].lower() for v in r if v['y']>.72 and v['x']<.5).replace('sucobat','swoobat').replace('suampert','swampert')
   prompt=prompt.replace('klink lang','klinklang')
   candidates=[n for n in policy if re.sub('[^a-z]','',n.lower())in re.sub('[^a-z]','',prompt) or any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.75 for w in prompt.split())]
   if len(candidates)!=1:print('ACTOR REVIEW',prompt,flush=True);break
   a.actor=candidates[0];plan=policy[a.actor];a.slot=plan['slot'];a.double=plan.get('double',plan.get('target') is not None);a.spread=plan.get('spread',a.spread);a.target=plan.get('target',1);a.hp_lower=plan.get('hp_lower',default_hp_lower)
  if not any(difflib.SequenceMatcher(None,a.actor.lower(),w).ratio()>=.72 for w in own.split()) or not any(difflib.SequenceMatcher(None,n,w).ratio()>=.78 for n in foes for w in enemy.split()):print('MATCHUP REVIEW',enemy,own,flush=True);break
  if turns>=a.turns:break
  rendered_field=None
  if a.auto_misty or a.require_field:
   from public_battle_field import observe
   rendered_field=observe(STATE);print('PUBLIC FIELD',rendered_field,flush=True)
   if rendered_field=='unknown' or (a.require_field and rendered_field!=a.require_field):print('PUBLIC FIELD REVIEW',flush=True);break
   if a.auto_misty:assert a.actor.lower()=='sylveon' and a.double and not a.spread
  if a.min_hp or a.heal_below or a.recover_below:
   imhp=Image.open(STATE).convert('RGB');ww,hh=imhp.size
   bl,br=(.761,.929) if a.hp_lower else ((.740,.908) if a.double else (.761,.929))
   fractions=[]
   for by in ([.655+i*.001 for i in range(32)] if a.hp_lower else ([.55+i*.001 for i in range(62)] if a.double else [.575+i*.001 for i in range(35)])):
    pixels=[imhp.getpixel((x,int(hh*by))) for x in range(int(ww*bl),int(ww*br))]
    fractions.append(sum((g>75 and g>r*1.3 and g>b*1.3) or (r>130 and b<70 and g<220) for r,g,b in pixels)/len(pixels))
   filled=max(fractions)
   print('HP BAR',round(filled,2),flush=True)
   if recovery_before is not None:
    if filled<=recovery_before+.01:
     print('RECOVERY DID NOT IMPROVE HP; REVIEW MATCHUP',flush=True);break
    recovery_before=None
   # Move-based healing can be outsped; honor the stop floor before selecting it.
   if a.recover_below and filled<a.recover_below and filled<a.min_hp:
    print('LOW HP BEFORE RECOVERY MOVE; REVIEW MATCHUP',own,flush=True);break
   if a.recover_below and filled<a.recover_below:
    if heals>=8:print('RECOVERY BUDGET REVIEW',flush=True);break
    recovery_before=filled
    subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),str(a.recover_slot),'--watch'],check=True)
    heals+=1;turns+=1;continue
   if a.heal_below and filled<a.heal_below:
    if heals>=6:print('HEAL BUDGET REVIEW',flush=True);break
    if subprocess.call([sys.executable,str(ROOT/'scripts/battle_item.py'),a.heal_item,a.actor]):break
    heals+=1;turns+=1
    continue
   if filled<a.min_hp:print('LOW HP REVIEW',own,flush=True);break
  if a.cure_sleep and re.search(r'\bslp[a-z]*\b',own):
   if cures>=4:print('SLEEP CURE BUDGET REVIEW',flush=True);break
   if subprocess.call([sys.executable,str(ROOT/'scripts/battle_item.py'),'Full Heal',a.actor]):break
   cures+=1;turns+=1;continue
  if foe_slots:
   matched=[n for n in foes if any(difflib.SequenceMatcher(None,n,w).ratio()>=.78 for w in enemy.split())]
   if len(matched)!=1 or matched[0] not in foe_slots:print('MOVE POLICY REVIEW',flush=True);break
   a.slot=int(foe_slots[matched[0]])
  if turns>=a.turns:break
  casting_misty=a.auto_misty and rendered_field=='inverse'
  opening=[n for n in openers if n not in opened and any(difflib.SequenceMatcher(None,n.lower(),w).ratio()>=.78 for w in enemy.split())]
  if opening:
   assert len(opening)==1
   opener=opening[0];a.slot=int(openers[opener]);opened.add(opener)
   print('REVIEWED OPENING MOVE',opener,a.slot,flush=True)
  cmd=[sys.executable,str(ROOT/'scripts/battle_move.py'),str(1 if casting_misty else a.slot)]
  if a.double and not a.spread and not casting_misty:cmd.append(str(a.target))
  if a.watch:cmd.append('--watch')
  command_start=time.time()
  rc=subprocess.call(cmd)
  if rc:raise SystemExit(rc)
  receipt=ROOT/'work/fast-chest-transition.json'
  if os.environ.get('REBORN_FAST_CHEST_TRANSITION')=='1' and receipt.exists() and json.loads(receipt.read_text())['epoch']>command_start:
   print('FAST INTERCEPTION FINISHED; review next battle',flush=True);break
  turns+=1;blank=0;continue
 imbottom=Image.open(STATE).convert('RGB');ww,hh=imbottom.size
 patch=imbottom.crop((int(ww*.08),int(hh*.75),int(ww*.90),int(hh*.87)))
 has_textbox=sum(min(px)>235 and max(px)-min(px)<5 for px in patch.getdata())/(patch.width*patch.height)>.55
 if has_textbox and any(v['y']>.72 and len(v['text'])>2 for v in r):
  bottom=' '.join(v['text'] for v in r if v['y']>.72)
  act('wait:0.7');now=' '.join(v['text'] for v in snap() if v['y']>.72)
  if difflib.SequenceMatcher(None,bottom,now).ratio()>.8:act('c','wait:0.4')
  blank=0;continue
 blank+=1
 if a.world_pause and turns>0 and not has_hud and not has_textbox:
  from PIL import ImageStat
  brightness=sum(ImageStat.Stat(Image.open(STATE).convert('RGB')).mean)/3
  if brightness>30:
   if os.environ.get('REBORN_FAST_CHEST_TRANSITION')=='1':
    from fast_chest_transition import finish
    finish()
    print('FAST MAP FALLBACK FINISHED; public end verification required',flush=True)
    break
   from chest_safe_pause import classify,finish_bag_entry
   route_file=os.environ.get('REBORN_POST_BATTLE_ROUTE')
   if route_file:
    steps=json.loads(pathlib.Path(route_file).read_text());assert 0<len(steps)<=100
    seq=[]
    for step in steps:
     key=step['key'];assert key in ['up','down','left','right','jump:up','jump:down','jump:left','jump:right'] and not step.get('action')
     seq += [key.removeprefix('jump:')+':.08']
     delay=float(step.get('wait',.35 if key.startswith('jump:') else .075));assert .05<=delay<=2
     seq += ['wait:'+str(delay)]
    subprocess.run([str(ROOT/'scripts/key_fast'),*seq,'wait:.6'],check=True)
    postrows=snap();posttext=' '.join(v['text']for v in postrows).lower()
    if any(v['y']>.72 and len(v['text'])>10 for v in postrows) or any(w in posttext for w in ['fight','wild','would like']):
     print('POST-ROUTE PUBLIC INTERRUPTION',posttext,flush=True);break
   post=os.environ.get('REBORN_POST_BATTLE_MOVES','').split(',')
   if post!=['']:
    assert len(post)<=12 and all(k in ['up','down','left','right']for k in post)
    subprocess.run([str(ROOT/'scripts/key_fast'),*[v for k in post for v in (k+':.12','wait:.10')]],check=True)
   act('x:.12','wait:.3','c:.12','wait:1.5')
   finish_bag_entry()
   print('ACTUAL BAG PAUSE',flush=True);break
 if blank>=2:
  im=Image.open(STATE).convert('RGB');w,h=im.size;box=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
  if sum(min(p)>235 and max(p)-min(p)<5 for p in box.getdata())/(box.width*box.height)>.55:
   act('c','wait:0.5');blank=0;continue
 if blank>=(2 if won else (2 if a.wild else 8)):print('OVERWORLD OR ANIMATION REVIEW',flush=True);break
 act('wait:1')
