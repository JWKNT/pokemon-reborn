"""Bounded normal-UI capture loop for reviewed Swords legends and Landorus and Amoonguss."""
from play import *
from PIL import Image
import difflib
foe=sys.argv[1];limit=int(sys.argv[2]);assert foe in ['Terrakion','Keldeo','Landorus','Thundurus'] and 1<=limit<=8
balls=0;recoveries=0
for turn in range(limit*3):
 rows=snap();t='\n'.join(x['text'] for x in rows);low=t.lower();print(t,flush=True)
 if any(s in low for s in ['gotcha','was caught','nickname','pokedex','add to your']):print('CAPTURE DECISION STOP',flush=True);break
 assert 'fight' in low and re.search(r'\b(?:bag|bae)\b',low), 'Command review: '+t
 enemy=' '.join(x['text'] for x in rows if x['y']<.37).lower()
 assert any(difflib.SequenceMatcher(None,foe.lower(),w.strip('.,')).ratio()>.78 for w in enemy.split()),enemy
 assert 'amoonguss' in re.sub('[^a-z]','',low), 'Actor review'
 im=Image.open(STATE).convert('RGB');w,h=im.size
 filled=max(sum((g>75 and g>r*1.3 and g>b*1.3) or (r>130 and b<70 and g<220) for r,g,b in [im.getpixel((x,int(h*y))) for x in range(int(w*.761),int(w*.929))])/(int(w*.929)-int(w*.761)) for y in [.575+i*.001 for i in range(35)])
 print('CAPTURE HP',round(filled,2),'balls',balls,flush=True)
 if filled<.52:
  assert filled>.22 and recoveries<2,'Low HP/recovery budget review'
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'1','--watch'],check=True);recoveries+=1;continue
 if balls>=limit:print('BALL BUDGET STOP',flush=True);break
 # The small animated HUD is also read as SLFF/HP or SLPF/HP.
 # Match only a sleep-status abbreviation at the enemy HUD, not dialogue.
 if not re.search(r'\bsl(?:p|f)[a-z]*/?\s*(?:hp)?',enemy):
  subprocess.run([sys.executable,str(ROOT/'scripts/battle_move.py'),'0','--watch'],check=True);continue
 subprocess.run([sys.executable,str(ROOT/'scripts/throw_ball.py'),'Timer Ball'],check=True);balls+=1
else:raise SystemExit('Capture action budget review')
