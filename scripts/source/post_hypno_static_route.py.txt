"""Source-only HYPOTHETICAL758 route proof, never observed gameplay evidence.

Reads extracted map/event JSON only; no game/save/native/UI/control imports or
inputs. Outputs a new proposal underwork. Pass --taka for the826True branch.
"""
import json,sys,copy,pathlib
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from void_static_paths import path
from post_hypno_exit import prefix_at_first_touch,FOLLOW
source=json.load(open(root/'work/void-source-event-index.json'));src={e['id']:e for m in source if m['map']==758 for e in m['events']};base=json.load(open(root/'work/void-map-758.json'))
state={'variables':{'391':30},'switches':{'1874':True,'826':'--taka' in sys.argv,'878':False},'self_switches':{'758,17,A':True}}
def cond(c,eid):
 return ((not c['switch1_valid'] or state['switches'].get(str(c['switch1_id']),False)) and(not c['switch2_valid'] or state['switches'].get(str(c['switch2_id']),False)) and(not c['variable_valid'] or state['variables'].get(str(c['variable_id']),0)>=c['variable_value']) and(not c['self_switch_valid'] or state['self_switches'].get(f'758,{eid},{c["self_switch_ch"]}',False)))
def model(start):
 v=copy.deepcopy(base);v['position']=list(start)
 for eid,event in src.items():
  pages=[p for p in event['pages'] if cond(p['condition'],eid)]
  if not pages:v['events'].pop(str(eid),None);continue
  p=pages[-1];old=v['events'].setdefault(str(eid),{'x':event['x'],'y':event['y'],'name':event['name']});old.update(list=p['list'],trigger=p['trigger'],through=p['through'],character=p['graphic']['character_name'],tile_id=p['graphic']['tile_id'])
 if state['self_switches'].get('758,90,A'):v['events']['25'].update(character='',through=True)
 if state['variables']['391']>=33:v['events']['26'].update(character='',through=True)
 return v
def finish(eid,pg=None):
 if pg is None:pg=[p for p in src[eid]['pages'] if cond(p['condition'],eid)][-1]
 for c in pg['list']:
  if c['indent']:continue
  a=c['parameters']
  if c['code']==123:state['self_switches'][f'758,{eid},{a[0]}']=a[1]==0
  if c['code']==122 and a[0]==a[1] and a[2:4]==[0,0]:state['variables'][str(a[0])]=a[4]
  if c['code']==121 and a[0]==a[1]:state['switches'][str(a[0])]=a[2]==0
 if eid in FOLLOW:
  f,pi=FOLLOW[eid];finish(f,src[f]['pages'][pi])
start=(28,102);ledger=[]
for phase,eid,goal in [('zel',33,(11,146)),('shade',34,(17,180)),('luna',35,(40,176))]:
 for _ in range(40):
  v=model(start);keys,nodes=path(v,start,goal);keys,nodes,stop=prefix_at_first_touch(v,nodes,keys,84,phase)
  start=nodes[-1];ledger.append({'phase':phase,'steps':len(keys),'end':start,'touch':stop[0] if stop else None,'hypothetical_story391':state['variables']['391']})
  if stop:
   finish(stop[0])
   if stop[0]==35:break
  if start==goal:
   if eid!=35:finish(eid)
   break
 else:raise RuntimeError('model iteration limit')
print('Hypothetical static route passed:',len(ledger),'chunks;',sum(x['steps']for x in ledger),'steps; touches', [x['touch']for x in ledger if x['touch']]);print('final hypothetical391',state['variables']['391'],'flag keys',[k for k,v in state['self_switches'].items()if v])
suffix='-taka' if '--taka' in sys.argv else ''
(root/f'work/post-hypno-static-route-proposal{suffix}.json').write_text(json.dumps({'proposal_only':True,'no_observed_completion':True,'no_ui_or_native_reads':True,'hypothetical_start':[758,28,102],'hypothetical_flags':{'391':30,'1874':True,'826':'--taka' in sys.argv,'878':False,'758,17,A':True},'ledger':ledger},indent=2)+'\n')
