from play import *
act('c')
blank=0
for i in range(30):
 r=snap();txt=' '.join(v['text'] for v in r);print(txt,flush=True)
 if any(w in txt.lower() for w in ['fight','sent out','would like to battle','choose a pok','pp:','fainted']):raise SystemExit('Battle interrupted healing; stop')
 if 'hope to see' in txt.lower() or 'fully healed' in txt.lower():act('c','wait:0.5');break
 if any(v['y']>.73 for v in r):act('c','wait:0.8')
 else:
  blank+=1
  if blank>=3:raise SystemExit('No nurse dialogue; position review')
  act('wait:1')
