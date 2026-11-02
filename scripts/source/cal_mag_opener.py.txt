"""Execute the reviewed Sturdy opener using public HUDs and normal inputs only."""
from play import *
import difflib,re

def resembles(name,text):
    return any(difflib.SequenceMatcher(None,name.lower(),re.sub('[^a-z]','',word.lower())).ratio()>=.74 for word in text.split())

last_actor=None
counts={'Boldore':0,'Mienshao':0,'Arcanine':0}
for cycle in range(60):
    rows=snap();text=' '.join(r['text'] for r in rows);low=text.lower()
    print(text,flush=True)
    control=ROOT/'notes/battle-control.json'
    if control.exists() and json.loads(control.read_text()).get('stop'):
        print('STOP REQUESTED',flush=True);break
    if any(x in low for x in ['out of usable','send in','switch your','change pok','trying to learn','defeated','derfeated']):
        print('OPENER BOUNDARY REVIEW',flush=True);break
    if 'cancel' in low and low.count('hp')>=5:
        next_actor={'Boldore':'Mienshao','Mienshao':'Arcanine'}.get(last_actor)
        if not next_actor:raise SystemExit('Unexpected forced switch')
        subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),next_actor],check=True)
        continue
    if 'fight' in low and 'bag' in low and 'run' in low:
        foes=' '.join(r['text'] for r in rows if r['y']<.37)
        if not resembles('Magmortar',foes):
            print('MAGMORTAR OPENER COMPLETE OR NEW FOE',flush=True);break
        prompt=' '.join(r['text'] for r in rows if r['y']>.72 and r['x']<.5)
        actors=[n for n in counts if resembles(n,prompt)]
        if len(actors)!=1:raise SystemExit('Actor review: '+prompt)
        actor=actors[0]
        if last_actor is None and actor!='Boldore':raise SystemExit('Full Sturdy opener must start with Boldore')
        if counts[actor]>=({'Boldore':2,'Mienshao':3,'Arcanine':1}[actor]):
            print('OPENER MOVE BUDGET REVIEW',flush=True);break
        slot=1 if actor=='Boldore' else (2 if actor=='Arcanine' or counts[actor]==0 else 3)
        print('REVIEWED OPENER ACTION',actor,slot,flush=True)
        subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),str(slot),'--watch'],check=True)
        counts[actor]+=1;last_actor=actor
        continue
    if re.search(r'\b(?:yes|no)\b',low):raise SystemExit('Unexpected choice')
    act('wait:.6')
else:raise SystemExit('Opener observation budget exhausted')
print('OPENER COUNTS',json.dumps(counts),flush=True)
