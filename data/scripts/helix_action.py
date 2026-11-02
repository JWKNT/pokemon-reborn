"""Helix normal controls; navigation notes reflect completed public interactions only."""
import json,subprocess,sys,time,re,difflib
from pathlib import Path
from play import act,read,ROOT
from locate import locate
P=ROOT/'notes/navigation-state.json'
static=json.loads((ROOT/'work/345-helix-static.json').read_text())['events']
def run(script,*a):
 for attempt in range(4):
  result=subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*map(str,a)])
  if result.returncode==0:return
  if result.returncode!=2 or script not in ['q','eventq']:raise subprocess.CalledProcessError(result.returncode,result.args)
  text=read();norm=lambda t:re.sub('[^a-z]','',t.lower().replace('Pokemon Reborn'.lower(),''))
  observed=norm(text);matches=[]
  for eid in [85,192,199,200,201]:
   page=static[str(eid)]['pages'][0]
   assert not any(c['code'] in [102,103,104,301] or any(k in str(c) for k in ['pbTrainerBattle','pbWildBattle','pbDoubleTrainerBattle']) for c in page['list'])
   score=max([difflib.SequenceMatcher(None,observed,norm(c['parameters'][0].replace('\\v[38]','Aster'))).ratio() for c in page['list'] if c['code']==101] or [0])
   matches.append((score,eid))
  score,eid=max(matches);assert score>.65,('Unexpected route interruption',text)
  print('HELIX INCIDENTAL SCENE',eid,text,flush=True)
  subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),'887',str(eid),'--source-page','0','--burst'],check=True)
  state=json.loads(P.read_text());state['self_switches'][f'887,{eid},A']=True;P.write_text(json.dumps(state,indent=2)+'\n')
 raise RuntimeError('Too many incidental scene interruptions')
def save_notes(state,evidence):
 state['self_switches'].update(json.loads(P.read_text()).get('self_switches',{}))
 state['helix_observation']={'epoch':time.time(),'evidence':evidence}
 P.write_text(json.dumps(state,indent=2)+'\n')
command=sys.argv[1]
s=json.loads(P.read_text());assert s['variables']['664']==3,'Puzzle-only helper'
if command=='swap':
 before=locate(887);assert before[0]==887
 was=s['switches'].get('1808',False);destid='30' if was else '31';leaveid='31' if was else '30'
 expected=tuple(s['positions']['887'][destid]);act('a','wait:2');after=locate(887)
 assert after==(887,*expected),(after,expected)
 s['switches']['1808']=not was;s['positions']['887'][leaveid]=list(before[1:]);s['positions']['887'][destid]=[1,1]
 save_notes(s,f'Normal A switch observed {before} -> {after}')
elif command=='approach':
 from nav import route
 eid=int(sys.argv[2]);a,x,y=locate(887);assert a==887
 v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),'887',str(x),str(y)],stderr=subprocess.DEVNULL));e=v['events'][str(eid)];options=[]
 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
  target=(e['x']+dx,e['y']+dy)
  try:options.append((len(route(v,target)),target))
  except ValueError:pass
 assert options,'No reachable side'
 _,target=min(options);run('q',f'887,{target[0]},{target[1]}')
else:
 eid=int(sys.argv[2]);e=static[str(eid)];name=e['name']
 crystal=name.startswith('Crystal');orb=name.startswith('EBall');snow=name.startswith('Abomasnow');clear=name.startswith('Altaria')
 assert crystal or orb or snow or clear,name
 run('eventq',887,eid,'talk')
 if snow or clear:
  run('choose_dialog','Yes|No','Yes');run('linear_dialog',887,eid,'--source-page',0,'--after-last-choice','--past-choice','--burst')
  s['switches'].update({'1809':snow,'1810':clear})
 else:
  page=0 if crystal or eid==45 else 1
  run('linear_dialog',887,eid,'--source-page',page,'--burst',*(['--world-settle','20'] if eid==48 else []))
  switches={c['parameters'][0] for c in e['pages'][page]['list'] if c['code']==121 and c['parameters'][0]==c['parameters'][1] and c['parameters'][2]==0}
  assert len(switches)==1,switches
  s['switches'][str(next(iter(switches)))]=True
 after=locate(887);assert after[0]==887
 save_notes(s,f'Completed normal interaction {eid} {name}; observed overworld {after}')
print('HELIX ACTION VERIFIED',command,sys.argv[2:],flush=True)
