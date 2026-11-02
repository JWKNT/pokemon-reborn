"""Start a reviewed major encounter and stop at its first command menu."""
from play import *
from PIL import Image
import argparse
p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('session',type=int);p.add_argument('map',type=int);p.add_argument('event',type=int);p.add_argument('--status',required=True);p.add_argument('--active-dialogue',action='store_true');p.add_argument('--continuity-proof');p.add_argument('--resume',action='store_true');p.add_argument('--touch-direction',choices=['up','down','left','right']);a=p.parse_args()
cfg=json.loads(pathlib.Path(a.config).read_text())
if a.touch_direction:
 assert not a.active_dialogue and not a.resume and (not a.continuity_proof or cfg.get('gauntlet_id') in ['hard-route-league','helix','aegir','anna-final'])
 from locate import locate
 mid,x,y=locate(a.map)
 source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL))['events'][str(a.event)]
 dx,dy={'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[a.touch_direction]
 assert source['trigger']==1 and (source['x'],source['y'])==(x+dx,y+dy),'Exact adjacent player-touch source required'
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
start_args=['start',a.config,a.session,'--status',a.status]
if a.continuity_proof:
 assert cfg.get('gauntlet_id') in ['hard-route-league','orphanage-memory','helix','aegir','anna-final'] or a.active_dialogue and (cfg['id'] in [113,114] or (cfg.get('gauntlet_id')=='glass' and cfg.get('gauntlet_round')in[2,3]) or (cfg.get('gauntlet_id')=='agate' and cfg.get('gauntlet_round')==2 and cfg['trainer_key']==['Solaris','Solaris',2]))
 start_args+=['--continuity-proof',a.continuity_proof]
if a.resume:
 assert a.active_dialogue
 rows=json.loads((ROOT/'recordings/major-fights'/f'session-{a.session:03}-attempts.json').read_text());row=rows[-1]
 assert row['id']==cfg['id'] and 'end' not in row
 music=json.loads((ROOT/'work/active-trainer-music.json').read_text());assert music['name']==cfg['opponent']
 intro=bool(row.get('battle_intro_evidence'));choice_done=False
else:
 run('major_attempt',*start_args)
 run('trainer_music','start',cfg.get('audio_class',(cfg.get('trainer_keys') or [cfg['trainer_key']])[-1][0]),cfg['opponent'],*(['--battle-track',cfg['battle_track']]if cfg.get('battle_track')else[]))
 if a.touch_direction:act(a.touch_direction+':.12','wait:.6')
 elif not a.active_dialogue:run('eventq',a.map,a.event,'talk')
 intro=False;choice_done=False
expected_choices=cfg.get('intro_choices') or ([cfg['intro_choice']]if cfg.get('intro_choice')else[])
choice_progress=0
if a.resume:choice_progress=row.get('intro_choice_progress',0)
if expected_choices:
 event=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(a.map),'0','0'],stderr=subprocess.DEVNULL))['events'][str(a.event)]
 if cfg.get('intro_choice_source'):
  choice_source=cfg['intro_choice_source']
  assert choice_source['map']==a.map and choice_source['page']>=1
  full=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(a.map),str(choice_source['event'])],stderr=subprocess.DEVNULL))
  linked=full['pages'][choice_source['page']-1];condition=linked['condition']
  assert linked['trigger']==3 and condition['variable_valid'],'Reviewed linked autorun required'
  expected=[condition['variable_id'],condition['variable_id'],0,0,condition['variable_value']]
  assert any(c['code']==122 and c['parameters']==expected for c in event['list']),'Entry event must activate the reviewed choice page'
  event=linked
 if cfg.get('recorded_intro_checkpoint'):
  assert cfg['id']==134 and a.active_dialogue and a.map==808 and a.event==19
  # The normal save predates the trigger variable; inspect its installed autorun page.
  full=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'808','19']))
  event=full['pages'][1]
 source_choices=[c['parameters'][0]for c in event['list']if c['code']==102]
 assert source_choices==[c['labels']for c in expected_choices], 'Configured introduction choices differ from installed event'
# Resolve reviewed introduction choices with the choice helper, which checks
# cropped native pixels when full-screen OCR misses a short Yes/No label.
# Do this before the general text advancer can accept an unseen default.
if expected_choices and not a.resume:
 for choice in expected_choices:
  run('choose_dialog','|'.join(choice['labels']),choice['answer'])
  choice_progress+=1
  path=ROOT/'recordings/major-fights'/f'session-{a.session:03}-attempts.json'
  records=json.loads(path.read_text());assert records[-1]['id']==cfg['id'] and 'end'not in records[-1]
  records[-1]['intro_choice_progress']=choice_progress
  path.write_text(json.dumps(records,indent=2)+'\n')
for _ in range(180):
 t=read();print(t,flush=True);low=t.lower();compact=re.sub('[^a-z]','',low)
 custom_intro = cfg.get('trainer_key')==['CHILDLIN','Lin',0] and cfg.get('intro_name')=='Arceus' and 'arceus' in compact and 'herepuppygogetem' in compact and 'hp' in compact
 title_line = bool(cfg.get('intro_title_line')) and re.sub('[^a-z]','',cfg['intro_title_line'].lower()) in [re.sub('[^a-z]','',z.lower()).replace('amerthyst','amethyst') for z in t.splitlines()]
 if (title_line or custom_intro or re.search('[wmuv]ouldliketobattle',compact) or re.search(r'\bvs\b',low) or (cfg.get('intro_name',cfg['opponent']).lower() in low and 'sentout' in compact)) and not intro:
  run('major_battle_intro',a.config,a.session);intro=True
 # Bind a later public challenge when the VS card opened the battle interval.
 # Native log creation can fall between these two recorded public events.
 if intro and re.search('[wmuv]ouldliketobattle',compact) and cfg['opponent'].lower() in low:
  path=ROOT/'recordings/major-fights'/f'session-{a.session:03}-attempts.json'
  records=json.loads(path.read_text());row=records[-1]
  if 'battle_challenge_epoch' not in row:
   public_rows=[json.loads(line) for line in (ROOT/'recordings/screens.jsonl').read_text().splitlines()[-5:]]
   matches=[r for r in public_rows if re.search('[wmuv]ouldliketobattle',re.sub('[^a-z]','',' '.join(r['text']).lower())) and cfg['opponent'].lower() in ' '.join(r['text']).lower()]
   if matches:
    evidence=matches[-1];epoch=evidence['epoch']
    if row['battle_start_epoch']<=epoch<=row['battle_start_epoch']+30:
     row['battle_challenge_epoch']=epoch;row['battle_challenge_evidence']=evidence
     path.write_text(json.dumps(records,indent=2)+'\n')
 grid=sum(n in low for n in ['extreme speed','crunch','flanethrouer','flamethrower','morning sun','trick room','destiny bond','waterfall','earthquake','light screen','discharge','freeze-dry','freeze-d','ice beam','ice bean','recover','recouer','high jump kick','wide guard','fake out','u-turn','signal beam'])>=2
 if intro and (grid or re.search(r'pp.?\s*\d+',low)):
  act('x','wait:.6');t=read();print(t,flush=True)
  assert 'fight' in t.lower() or 'what will' in t.lower(),'Move grid cancel needs review'
  print('FIRST BATTLE COMMAND READY (grid cancelled)',flush=True);break
 if ('fight' in low or 'what will' in low) and re.search(r'(?<![a-z])f?hp(?![a-z])',low):
  assert intro,'Battle began without an observed introduction'
  print('FIRST BATTLE COMMAND READY',flush=True);break
 choice_labels={label.lower()for choice in expected_choices for label in choice['labels']}|{'yes','no'}
 if any(v.strip().lower() in choice_labels for v in t.splitlines()):
  assert choice_progress<len(expected_choices) and not intro,'Unexpected intro choice'
  choice=expected_choices[choice_progress]
  run('choose_dialog','|'.join(choice['labels']),choice['answer']);choice_progress+=1
  path=ROOT/'recordings/major-fights'/f'session-{a.session:03}-attempts.json'
  records=json.loads(path.read_text());assert records[-1]['id']==cfg['id'] and 'end'not in records[-1]
  records[-1]['intro_choice_progress']=choice_progress;path.write_text(json.dumps(records,indent=2)+'\n')
  continue
 if 'choose a pok' in low or 'out of usable' in low:raise SystemExit('Unexpected intro state')
 im=Image.open(STATE).convert('RGB');w,h=im.size;box=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 # A dense two-line caption can occupy most of the text crop. Its left
 # white gutter remains visible and distinguishes it from the overworld.
 gutter=im.crop((int(w*.09),int(h*.755),int(w*.10),int(h*.875)))
 textbox=(sum(min(z)>235 and max(z)-min(z)<5 for z in box.getdata())/(box.width*box.height)>.55 or
          sum(min(z)>235 and max(z)-min(z)<5 for z in gutter.getdata())/(gutter.width*gutter.height)>.9)
 try:
  # The QMARK dream scene deliberately uses glyphs OCR cannot decode.
  glyph_dialogue = (((cfg.get('gauntlet_id')=='glass' and cfg.get('gauntlet_round') in [2,3]) or cfg.get('reviewed_ellipsis_intro')) and textbox and sum(max(z)<180 for z in box.getdata())/(box.width*box.height)>.0002)
  if textbox and (len(t.replace('Pokemon Reborn','').strip())>=2 or glyph_dialogue):act('c','wait:.35')
  else:act('wait:.5')
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  from locate import capture_ready
  capture_ready();print('CAPTURE RECOVERED; re-reading current intro state',flush=True)
else:raise SystemExit('Battle intro limit')
