"""Finish an already accepted ordinary Rock Climb and verify its reviewed landing."""
from play import *
from locate import locate
mid,x,y=map(int,sys.argv[1:4])
t=read();compact=re.sub('[^a-z]','',t.lower());print(t,flush=True)
if 'usedrockclimb' in compact:
 act('c','wait:5')
else:
 assert not any(z in compact for z in ['fight','yes','nastyplot','wouldyou','chooseapok']), 'Unexpected climb prompt: '+t
actual=locate(mid);assert actual==(mid,x,y),(actual,(mid,x,y))
print('ROCK CLIMB LANDING VERIFIED',actual,flush=True)
