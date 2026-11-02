"""Close a visibly won warmup at HUD disappearance, without advancing story."""
import argparse,json,re,subprocess,sys
from pathlib import Path
from play import ROOT,snap,act
from hypno_turn import name_matches

p=argparse.ArgumentParser();p.add_argument('journal',type=Path);p.add_argument('session',type=int);a=p.parse_args()
j=json.loads(a.journal.read_text());w=j['warmup'];assert w['session']==a.session and 'result' not in w
m=json.loads((ROOT/'work/active-trainer-music.json').read_text());assert m['class']=='NWOrderly' and m['name']=='Howaya & Christina'
rows=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()]
wins=[s for s in rows if s['epoch']>=w['battle_start_epoch'] and re.search(r'de.?feated|for winning',' '.join(s['text']),re.I)]
assert wins,'Actual recorded warmup victory required; no input sent'
names=[x.get('name') or x['species'] for x in j['before']['party']]
def own_hud(rows):
 text=' '.join(s['text'] for s in rows if s['x']>.5 and .35<s['y']<.73)
 return any(name_matches(text,n) for n in names) and bool(re.search(r'\bhp\b|l[uvụ][.?\s]*\d{1,3}',text,re.I))
for _ in range(40):
 s=snap();t=' '.join(x['text'] for x in s);print(t,flush=True)
 assert not re.search(r'\bfight\b|choose a pok|switch in|out of usable',t,re.I),'Unexpected battle input; stop'
 if not own_hud(s):
  act('wait:.7');assert not own_hud(snap()),'HUD transition still active';break
 act('c:.12','wait:.5')
else:raise SystemExit('Victory HUD closure limit')
subprocess.run([sys.executable,str(ROOT/'scripts/trainer_music.py'),'finish','--world-verified'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/agate_chain_archive.py'),'warmup-end',str(a.journal),'victory','--evidence-epoch',str(wins[0]['epoch'])],check=True)
print('WARMUP CLOSED; INTER-BATTLE STORY UNADVANCED; NO SAVE/REORDER/PC',flush=True)
