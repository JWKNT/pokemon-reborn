"""Reviewed city errands, normal dialogue and purchases; bounded, resumable blocks."""
from play import *
block=int(sys.argv[1]);assert 1<=block<=5

def r(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,a)],check=True)
def door(m,n):r('city_enter.py',m,n)
def fly(m):r('fly_to.py',m)
def recruit(m,e):r('recruit_volunteer.py',m,e)
def forest(s,*args):
 for attempt in range(30):
  begun=time.time();rc=subprocess.call([sys.executable,str(ROOT/'scripts'/s),*map(str,args)])
  if rc==0:return
  text=read().lower()
  # Malchous Forest Park was inspected: no trainer battles on this map.
  if 'fight' in text and 'hp' in text:
   r('flee.py','--since',begun);continue
  raise SystemExit('Forest route interruption requires review: '+text)
 raise SystemExit('Forest route retry bound')
if block==1:
 r('eventq.py',38,6,'enter');fly(526);door(526,613)
 r('eventq.py',613,5,'talk');r('dialog.py','--yes','--limit=100')
 r('checkpoint.py','Adrienn-recruitment-start')
 s=json.loads((ROOT/'notes/Adrienn-recruitment-start-navigation.json').read_text());assert s['variables']['339']==50
elif block==2:
 door(613,526);door(526,559);recruit(559,16);door(559,528);recruit(528,33)
 door(528,520);recruit(520,88);door(520,611);r('eventq.py',611,2,'talk');r('mart_open.py')
 r('shop_buy.py','Revival Herb',4,2800);r('mart_exit.py');door(611,520)
 door(520,570);recruit(570,2);door(570,520);fly(521);door(521,117);recruit(117,62)
 door(117,521);fly(527);recruit(527,76);fly(524);recruit(524,80)
 r('checkpoint.py','Adrienn-recruitment-seven')
 assert json.loads((ROOT/'notes/Adrienn-recruitment-seven-navigation.json').read_text())['variables']['339']==57
elif block==3:
 r('party_front.py','Cofagrigus');fly(530);recruit(530,94);door(530,53);recruit(53,10);door(53,530)
 door(530,531);recruit(531,3);door(531,530);door(530,522);door(522,594);recruit(594,5)
 door(594,522);r('checkpoint.py','Adrienn-recruitment-eleven')
 assert json.loads((ROOT/'notes/Adrienn-recruitment-eleven-navigation.json').read_text())['variables']['339']==61
elif block==4:
 fly(523);door(523,535);recruit(535,4);door(535,523);r('party_front.py','Cofagrigus')
 r('eventq.py',523,42,'enter');forest('eventq.py',533,22,'item')
 r('mark_event.py',533,22);fly(525);r('train_candy_one.py','Cofagrigus',3,'XL')
 r('checkpoint.py','Adrienn-Cofagrigus-trained')
 s=json.loads((ROOT/'notes/Adrienn-Cofagrigus-trained-status.json').read_text());cf=next(m for m in s['party']if m['species']=='COFAGRIGUS');assert cf['level']==80
elif block==5:
 r('connected_walk.py',525,543,30,10);recruit(543,42)
 r('connected_walk.py',543,525,0,10);r('connected_walk.py',525,544,23,17)
 door(544,548);recruit(548,17);door(548,544)
 r('connected_walk.py',544,525,21,23);r('connected_walk.py',525,551,15,12);recruit(551,18)
 r('checkpoint.py','Adrienn-all-volunteers')
 assert json.loads((ROOT/'notes/Adrienn-all-volunteers-navigation.json').read_text())['variables']['339']==65
print('REVIEWED CIRCUIT BLOCK COMPLETE',block,flush=True)
