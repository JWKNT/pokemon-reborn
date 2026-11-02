"""Normal nurse, explicit Cryo/Mien lead order, safe pre-double staging only."""
import argparse,json,sys,time
from agate_party_assemble import Runner,ROOT,need
from play import read
sp=ROOT/'notes/Agate-Antoine-won131-status.json';np=ROOT/'notes/Agate-Antoine-won131-navigation.json'
s=json.loads(sp.read_text());n=json.loads(np.read_text())
assert s['map']==763 and n['variables']['391']==52 and n['self_switches']['763,49,A'] is True
assert n['self_switches'].get('763,45,A',False) is False and n['self_switches'].get('763,46,A',False) is False
args=argparse.Namespace(journal=ROOT/'work/agate-double-prepare131-after-heal.json',status=sp,navigation=np,phase='approach',checkpoint='Agate-double-ready131')
r=Runner(args,s,n,{'phase':'ordinary-double-prep','trigger_not_entered':True})
try:
 r.settle();r.position(752) # completed native nurse not repeated; close only actual Pause
 r.arrange(('CRYOGONAL','MIENSHAO','COFAGRIGUS','ARCANINE','SWAMPERT','EXCADRILL'))
 r.active_source(752,8,0);r.run('eventq',752,8,'enter');r.position(763,(763,46,70))
 r.walk(41,56);r.party_check();r.run('checkpoint','Agate-double-ready131')
 final=json.loads((ROOT/'notes/Agate-double-ready131-status.json').read_text())
 assert final['position']==[41,56] and final['party'][0]['name']=='Hexan' and final['party'][1]['name']=='Mienshao'
 assert all(m['level']==90 and m['hp']==m['totalhp'] and m['status'] is None for m in final['party'])
 assert final['party'][0]['item']=='FOCUSSASH'
 r.journal.update(status='completed-safe-phase',verified=True);r.write()
 print('CRYO MIEN DOUBLE READY; NOTTRIGGERED',flush=True)
except BaseException as e:
 r.journal.update(status='stopped-for-actual-state-review',verified=False);r.record('stop',reason=str(e),error=type(e).__name__);raise
