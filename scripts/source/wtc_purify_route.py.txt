"""Recorded normal-input cleanup after an actual PULSE victory; restart by stage."""
from play import *
from locate import locate
from wtc_model import predict

stage=int(sys.argv[1])if len(sys.argv)>1 else 1
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
def purify(water):
 for _ in range(2):
  s=json.loads((ROOT/'notes/navigation-state.json').read_text())
  assert s['switches'].get('548'), 'Actual saved PULSE victory required'
  if s['variables'].get(str(water))==3:return
  mid,x,y=locate()
  v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),str(x),str(y)],stderr=subprocess.DEVNULL))
  controls=[int(eid)for eid,e in v['events'].items()if e['trigger']==0 and any(c['code']==122 and c['parameters'][0]==water for c in e['list']or[])and any(c['code']==201 for c in e['list']or[])]
  assert len(controls)==1,('Water control needs review',mid,controls)
  new,newmid,_=predict(s,mid,controls[0])
  assert new['variables'][str(water)]in[1,3]
  run('wtc_water',mid,controls[0],newmid)
 assert json.loads((ROOT/'notes/navigation-state.json').read_text())['variables'][str(water)]==3
def exit_to(dest):
 mid,_,_=locate()
 if mid!=dest:run('wtc_room_exit',mid,dest)
if stage<=1:
 purify(258);exit_to(469);purify(257)
 print('PURIFICATION STAGE 1 COMPLETE',flush=True)
if stage<=2:
 exit_to(472);purify(261);exit_to(471);purify(260)
 print('PURIFICATION STAGE 2 COMPLETE',flush=True)
if stage<=3:
 # The dirty-high North controller is reached from Opal's south entrance;
 # its eastern entrance is isolated until the water is clean.
 exit_to(498);exit_to(501);exit_to(480);purify(256)
 print('PURIFICATION STAGE 3 COMPLETE',flush=True)
if stage<=4:
 exit_to(474);purify(259);exit_to(468);purify(262)
 print('PURIFICATION STAGE 4 COMPLETE',flush=True)
if stage<=5:
 exit_to(502);exit_to(475);purify(263);exit_to(496);run('beryl_flush')
 print('PURIFICATION STAGE 5 COMPLETE',flush=True)
s=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert all(s['variables'].get(str(i))==3 for i in range(256,265))
print('ALL NINE WATER GRIDS PURIFIED',flush=True)
