"""Read-only stat estimates from installed base stats and the trainer construction rules."""
import json,re,sys,math
s=open('/Applications/Reborn.app/Contents/Game/Scripts/Reborn/montext.rb').read()
natures={'ADAMANT':(1,3),'BRAVE':(1,5),'LONELY':(1,2),'NAUGHTY':(1,4),'BOLD':(2,1),'RELAXED':(2,5),'IMPISH':(2,3),'LAX':(2,4),'MODEST':(3,1),'MILD':(3,2),'QUIET':(3,5),'RASH':(3,4),'CALM':(4,1),'GENTLE':(4,2),'SASSY':(4,5),'CAREFUL':(4,3),'TIMID':(5,1),'HASTY':(5,2),'JOLLY':(5,3),'NAIVE':(5,4)}
for p in json.load(open(sys.argv[1]))[0][1]:
 forms=json.load(open('work/installed-base-stats.json'))[p['species']];base=forms[p.get('form',0)].get('BaseStats',forms[0]['BaseStats']);lv=p['level'];iv=p.get('iv',10);ivs=[31]*5+[0] if iv==32 else [iv]*6;ev=p.get('ev',[min(85,lv*3//2)]*6).copy()
 if iv==32:ev[5]=0
 a=[(2*b+ivs[i]+ev[i]//4)*lv//100+(lv+10 if i==0 else 5) for i,b in enumerate(base)]
 if p.get('nature') in natures:
  u,d=natures[p['nature']];a[u]=a[u]*110//100;a[d]=a[d]*90//100
 print(p['species'],dict(zip(['HP','Atk','Def','SpA','SpD','Spe'],a)))
