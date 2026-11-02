"""Native route supplies and castle car maze from observed TrainTown exit."""
from play import *
def r(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
r('eventq',691,5,'item');r('eventq',691,6,'item');r('eventq',691,1,'item')
r('give_held','Amulet Coin','Cofagrigus')
r('eventq',691,2,'enter');r('settle_arrival',686)
r('room_follow',ROOT/'work/g15-car-maze-to-fairy.json')
r('eventq',686,29,'enter');r('settle_arrival',696)
print('FAIRY MAZE ARRIVAL COMPLETE',flush=True)
