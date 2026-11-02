"""Claim verified volunteer rewards, restore the six, heal, and save before Adrienn."""
from play import ROOT
import sys,subprocess,json
def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
nav=json.loads((ROOT/'notes/navigation-state.json').read_text());assert nav['variables']['339']==65
r('fly_to.py',526);r('city_enter.py',526,613);r('eventq.py',613,5,'talk');r('linear_dialog.py',613,5,'--active','--burst')
r('checkpoint.py','Adrienn-volunteers-rewarded')
nav=json.loads((ROOT/'notes/Adrienn-volunteers-rewarded-navigation.json').read_text());assert nav['variables']['339']==46
r('city_enter.py',613,526);r('city_enter.py',526,100)
r('eventq.py',100,7,'talk');r('pc_open_reviewed.py');r('pc_exchange_named.py',11,4,'Ampharos','Tranquill')
r('eventq.py',100,4,'talk');r('heal.py');r('party_front.py','Klinklang','Mienshao')
r('city_enter.py',100,526);r('city_enter.py',526,613);r('checkpoint.py','Adrienn-roster-ready')
s=json.loads((ROOT/'notes/Adrienn-roster-ready-status.json').read_text());p={m['species']:m for m in s['party']}
assert set(p)=={'KLINKLANG','MIENSHAO','ARCANINE','EXCADRILL','AMPHAROS','COFAGRIGUS'}
assert all(m['level']==80 and m['hp']==m['totalhp'] for m in s['party'])
assert p['KLINKLANG']['ev']==[252,252,3,0,0,0]and p['EXCADRILL']['ev']==[247,252,0,0,0,11]
assert s['bag']['contents']['REVIVALHERB']==4
print('ADRIENN ROSTER AND ITEMS VERIFIED; ENTER WITHIN120SECONDS OR REFRESH CHECKPOINT',flush=True)
