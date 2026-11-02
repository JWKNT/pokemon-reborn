"""Normal source-reviewed south entry; preserve Fly carrier; stop before Ricardo."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--status',default='notes/Agate-Cofa-prepared-status.json');p.add_argument('--navigation',default='notes/Agate-Cofa-prepared-navigation.json');a=p.parse_args()
s=json.loads((ROOT/a.status).read_text());n=json.loads((ROOT/a.navigation).read_text());c=s['party'][0]
assert s['map']==355 and n['variables']['391']==51 and n['switches']['988'] is True
assert c['species']=='COFAGRIGUS' and c['item'] is None and (c.get('natureflag') or c['nature'])=='TIMID' and c['ev']==[172,4,252,80,0,2]
assert c['hp']==c['totalhp']==252 and [m['move'] for m in c['moves']]==['TRICKROOM','HEX','WILLOWISP','DARKPULSE']
assert any(m['name']=='Tranquill' and m['hp']>0 and any(v['move']=='FLY' for v in m['moves']) for m in s['party'])
commands=[('use_field_item',['Super Repel']),('fly_to',[292]),('connected_walk',[292,291,48,0]),('connected_walk',[291,297,25,13]),('eventq',[297,1,'enter']),('q',['298,8,2']),('eventq',[298,8,'enter']),('checkpoint',['Agate-south-ready130'])]
if not a.execute:
 print(json.dumps({'proposal_only':True,'commands':commands,'stop':[763,36,85]},indent=2));raise SystemExit(0)
os.environ['REBORN_COORD_CACHE']='1';os.environ['REBORN_ROUTE_CHUNK']='84'
from play import read
from locate import locate
assert len(read().splitlines())<4 and locate()[0]==355
navpath=ROOT/'notes/navigation-state.json';nav=json.loads(navpath.read_text());assert nav['variables']['391']==51
avoid=nav.setdefault('avoid',{}).setdefault('291',[])
for tile in [[37,y] for y in range(19,26)]:
 if tile not in avoid:avoid.append(tile)
navpath.write_text(json.dumps(nav,indent=2)+'\n')
for name,args in commands:
 print('SOUTH ENTRY QUEUE',name,*args,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
after=json.loads((ROOT/'notes/Agate-south-ready130-status.json').read_text());assert after['map']==763 and after['position']==[36,85]
print('SOUTH ENTRY VERIFIED; STOP BEFORE RICARDO',flush=True)
