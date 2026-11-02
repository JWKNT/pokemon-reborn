from play import *
for i in range(80):
 t=read();print(i,t.replace('\n',' | '),flush=True);lo=t.lower()
 if 'woobat' in lo:break
 if 'fight' in lo:act('right','down','c','wait:2');continue
 if 'hp' in lo or any(w in lo for w in ['wild','safely','escape']):act('c','wait:1');continue
 if len(t.splitlines())<4:act('left:0.5' if i%2==0 else 'right:0.5','wait:0.5');continue
 print('Review');break
