"""Advance an inspected linear scene; refuse event assets containing choices/battles."""
from play import *
from PIL import Image
import re,difflib
m,e=map(int,sys.argv[1:3]);v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(m),str(e)],stderr=subprocess.DEVNULL))
cs=[c for p in v['pages'] for c in p['list']]
if '--active' in sys.argv:
 active=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(m),'0','0'],stderr=subprocess.DEVNULL))
 cs=active['events'][str(e)]['list']
if '--source-page' in sys.argv:
 page=int(sys.argv[sys.argv.index('--source-page')+1]);assert 0<=page<len(v['pages'])
 cs=v['pages'][page]['list']
range_stop=None;source_offset=0
if '--follow-source' in sys.argv:
 i=sys.argv.index('--follow-source');fm,fe=map(int,sys.argv[i+1:i+3])
 follow=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(fm),str(fe)],stderr=subprocess.DEVNULL))
 follow_pages=follow['pages']
 if '--follow-source-page' in sys.argv:
  follow_pages=[follow_pages[int(sys.argv[sys.argv.index('--follow-source-page')+1])]]
 cs.extend(c for page in follow_pages for c in page['list'])
if '--command-range' in sys.argv:
 i=sys.argv.index('--command-range');first,last=map(int,sys.argv[i+1:i+3])
 assert '--source-page' in sys.argv and 0<=first<=last<len(cs) and cs[last]['code']==101, 'Explicit source-page dialogue range required'
 assert not any(flag in sys.argv for flag in ['--after-last-battle','--after-last-choice','--follow-source']), 'Range cannot mix source slicing'
 range_stop=str(cs[last]['parameters'][0]);cs=cs[first:last+1];source_offset=first
if '--after-last-battle' in sys.argv:
 assert '--past-battle' in sys.argv,'Battle tail requires an observed completed victory'
 hits=[i for i,c in enumerate(cs)if any(k in str(c['parameters'])for k in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle'])]
 assert hits,'No installed battle boundary'
 source_offset=max(hits)+1;cs=cs[source_offset:]
until_choice='--until-choice' in sys.argv
if '--after-last-choice' in sys.argv:
 assert '--past-choice' in sys.argv, 'Choice tail requires an observed answered final choice'
 hits=[i for i,c in enumerate(cs) if c['code']==102]
 assert hits, 'No installed choice boundary'
 source_offset=max(hits)+1;cs=cs[source_offset:]
if '--after-last-choice' not in sys.argv and ('--past-choice' in sys.argv or until_choice) and sum(c['code']==102 for c in cs)!=1:raise SystemExit('Expected exactly one inspected choice')
if until_choice and next(c for c in cs if c['code']==102)['parameters'][0]!=['Yes','No']:raise SystemExit('Expected inspected Yes/No choice')
if any(c['code'] in ([103,104] if '--past-choice' in sys.argv or until_choice else [102,103,104]) or ('--past-battle' not in sys.argv and (c['code']==301 or any(k in str(c['parameters']) for k in ['pbTrainerBattle','pbDoubleTrainerBattle','pbWildBattle']))) for c in cs):raise SystemExit('Scene is not linear')
def textbox():
 im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
 white=sum(min(p)>235 and max(p)-min(p)<5 for p in b.getdata())/(b.width*b.height)>.35
 # RBY scenery is white and stylized shouts can evade OCR; use the box border.
 def darkrow(y):
  px=[im.getpixel((x,int(h*y))) for x in range(int(w*.08),int(w*.90))]
  return sum(max(z)<95 for z in px)/len(px)
 return white and max(darkrow(y) for y in [.721,.725,.729,.733])>.80 and max(darkrow(y) for y in [.895,.900,.905,.910])>.80
source_blocks=[];source_block_commands=[]
for command_index,command in enumerate(cs):
 if command['code']==101:
  source_blocks.append(str(command['parameters'][0]));source_block_commands.append(command_index)
 elif command['code']==401 and source_blocks:source_blocks[-1]+=' '+str(command['parameters'][0])
def known_dialog(text):
 # Installed Glass aftermath intentionally renders unreadable glyphs.
 if (m,e)==(734,12) and '--after-last-battle' in sys.argv:
  im=Image.open(STATE).convert('RGB');w,h=im.size;b=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
  pixels=list(b.getdata())
  if sum(min(z)>235 and max(z)-min(z)<5 for z in pixels)/len(pixels)>.55 and sum(max(z)<180 for z in pixels)/len(pixels)>.006:return True
 # Some WTC portraits/style overlays obscure the border. Recognize only a
 # matching installed scene line before sending C in such a box.
 norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
 n=norm(text)
 return len(n)>10 and any(difflib.SequenceMatcher(None,n,norm(b)).ratio()>.65 for b in source_blocks)
# A reviewed Yes/No boundary is safe to approach in short bursts, but never cross.
burst_cs=cs[:next(i for i,c in enumerate(cs) if c['code']==102)] if until_choice else cs
last_scene_text=None;repeat_scene_text=0
world_settle=6
if '--world-settle' in sys.argv:
 world_settle=int(sys.argv[sys.argv.index('--world-settle')+1]);assert 6<=world_settle<=90
# Optional audio anchors use text immediately following inspected BGM commands.
scripted_bgm=[];seen_bgm=set()
def scripted_bgm_track(command):
 if command['code']==242:return '__silence__'
 audio=command['parameters'][0]
 return audio['name'] if audio.get('name') and audio.get('volume',100)>0 else '__silence__'
if '--log-scripted-bgm' in sys.argv:
 for i,cmd in enumerate(cs):
  if cmd['code'] not in [241,242]:continue
  after=cs[i+1:];block=[]
  for z in after:
   if z['code']==101:
    if block:break
    block=[str(z['parameters'][0])]
   elif z['code']==401 and block:block.append(str(z['parameters'][0]))
  if block:
   track=scripted_bgm_track(cmd)
   scripted_bgm.append((i,' '.join(block),track))
# Optional inspected scene transition: explicitly log a scripted BGM fade.
fade_text=None;fade_seen=False
if '--log-bgm-fade' in sys.argv:
 for i,cmd in enumerate(cs):
  if cmd['code']==242:
   before=cs[:i];j=max(j for j,z in enumerate(before) if z['code']==101)
   fade_text=' '.join(str(z['parameters'][0]) for z in before[j:] if z['code'] in [101,401]);break
 if fade_text is None:raise SystemExit('No inspected BGM fade')
for _ in range(400):
 t=read();low=t.lower();print(t,flush=True)
 if range_stop:
  nstop=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
  if difflib.SequenceMatcher(None,nstop(t),nstop(range_stop)).ratio()>.80:
   print('INSPECTED RANGE END; final dialogue remains unadvanced',flush=True);break
 choice_rows=[re.sub(r'^[^a-z]+', '', v.strip().lower()) for v in t.splitlines()]
 if until_choice and any(z in choice_rows for z in ['yes','tes','ves','yee']) and any(z in choice_rows for z in ['no','ro','mo']):
  print('INSPECTED CHOICE READY',flush=True);break
 if scripted_bgm:
  normbgm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
  for idx,text_anchor,track in scripted_bgm:
   if idx in seen_bgm:continue
   if difflib.SequenceMatcher(None,normbgm(t),normbgm(text_anchor)).ratio()>.7:
    # Fade command has started by this text; retained playback uses a short crossfade.
    with (ROOT/'recordings/music-events.jsonl').open('a') as f:
     f.write(json.dumps({'epoch':time.time(),'bgm':{'name':track},'source':'inspected-scripted-BGM','map':m,'event':e,'command_index':idx+source_offset,'evidence':t})+'\n')
    seen_bgm.add(idx);print('SCRIPTED BGM',track,flush=True)
 repeat_scene_text=repeat_scene_text+1 if low==last_scene_text else 1
 last_scene_text=low
 # Nostra's installed memory intentionally ends in five identical text boxes.
 # Keep the ordinary stuck-dialogue guard elsewhere and bound this exact line.
 repeat_limit=7 if (m,e)==(898,283) and 'this outcome cannot be foreseen' in low else 4
 if len(low)>20 and repeat_scene_text>=repeat_limit:raise SystemExit('Repeated scene review')
 if re.search(r'\bhp\b|\bpp:',low) or ('yes' in low.splitlines() or 'choose a pok' in low):raise SystemExit('Scene guard')
 if not (textbox() or known_dialog(t)):
  for _settle in range((world_settle+2)//3):
   act('wait:3');t=read()
   if textbox() or known_dialog(t):break
  if not (textbox() or known_dialog(t)):print('OVERWORLD',flush=True);break
  continue
 n=1
 if '--burst' in sys.argv and not any(c['code']==102 for c in burst_cs):
  blocks=[]
  for cmd in burst_cs:
   if cmd['code']==101:blocks.append(str(cmd['parameters'][0]))
   elif cmd['code']==401 and blocks:blocks[-1]+=' '+str(cmd['parameters'][0])
  norm=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
  matches=[(difflib.SequenceMatcher(None,norm(t.replace('Pokemon Reborn','')),norm(b)).ratio(),i) for i,b in enumerate(blocks)]
  if matches:
   score,idx=max(matches)
   if score>.65:
    n=min(3,max(1,len(blocks)-idx-4))
    # Keep single presses around every music transition so its visible text
    # anchor cannot be crossed by a burst. This uses installed source only.
    for command_index,_,_ in scripted_bgm:
     anchor=next((j for j,start in enumerate(source_block_commands) if start>command_index),len(blocks))
     if abs(anchor-idx)<=8:n=1
 if fade_text and not fade_seen:
  normfade=lambda z:re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
  if difflib.SequenceMatcher(None,normfade(t),normfade(fade_text)).ratio()>.65:
   n=1;fade_seen=True
   (ROOT/'work/active-scene-silence.json').write_text(json.dumps({'start_epoch':time.time()+.7,'map':m,'event':e,'evidence':t}))
  # Single-step close to the fade so the anchor cannot be skipped by a burst.
  elif any(q in low for q in ['everything changed','make them leave']):n=1
 try:act(*sum((['c','wait:0.35'] for _ in range(n)),[])) # Stay single-step near the end of the inspected scene.
 except subprocess.CalledProcessError as error:
  if error.returncode!=2:raise
  recovered=False
  for _ in range(30):
   health=json.loads((ROOT/'recordings/capture-health.json').read_text())
   recovered=health.get('active') and time.time()-health.get('epoch',0)<2
   if recovered:break
   time.sleep(.5)
  if not recovered:raise
  print('CAPTURE RECOVERED; inspecting current dialogue without replaying inputs',flush=True)
else:raise SystemExit('Scene limit')
