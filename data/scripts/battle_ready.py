"""Wait for a safe battle input screen after a switch; choose no action."""
from play import *
from PIL import Image
import re,difflib
last='';same=0;no_hud=0
for _ in range(40):
    t=read();low=t.lower();print(t,flush=True)
    if re.search(r'de.?feated|for winning',low):
        print('VICTORY — stopped before inter-battle story',flush=True);break
    if ('fight' in low and re.search(r'\b(?:bag|bae)\b',low)) or ('what will' in low and re.search(r'\b(?:bag|bae)\b',low) and 'run' in low):break
    if 'trying to learn' in ' '.join(low.split()):
        from learning import resolve
        if not resolve(t):raise SystemExit('Unplanned learning prompt: review required')
        continue
    if 'abouttosendin' in re.sub('[^a-z]','',low):
        act('c','wait:.5');continue
    if 'use next pok' in low:raise SystemExit('Forced replacement: review before any further input')
    if 'choose a pok' in low or ('cancel' in low and low.count('hp')>=5) or 'out of usable' in low:break
    if 'no pp left' in low:
        act('c','wait:.3','x','wait:.3');raise SystemExit('Exhausted move: no battle action advanced; returned to command')
    if 'switch in' in low and 'summary' in low and 'cancel' in low:
        raise SystemExit('Unconfirmed named replacement; review Switch In menu')
    # A briefly obscured command label can cause a message-advance tap to open
    # Fight. Cancel that grid before choosing anything; readiness never attacks.
    if 'pp:' in low or re.search(r'pp.?\s*\d+\s*[/0]\s*\d+',low):
        act('x:0.08','wait:.3');print('CANCELLED MOVE GRID; re-reading command',flush=True);continue
    if 'change pok' in low or 'switch your' in low:raise SystemExit('Unexpected battle input screen')
    # These ordinary EXP/stat confirmations each accept one advance; waiting
    # for four identical observations adds idle time after every level gained.
    if re.search(r'grew to level\s*\d+',low) or (('max. hp' in low or 'max.hp' in low) and 'attack' in low and 'defense' in low):
        act('c','wait:.4');continue
    # A fast victory card can pass between OCR samples. Do not advance
    # post-battle story merely because the standard victory line was missed.
    hud=bool(re.search(r'\bhp\b|l[uvwy][.\s]?\d{1,3}|\d+\s*/\s*\d+',low))
    no_hud=0 if hud else no_hud+1
    if no_hud>=2:
        print('NO COMBAT HUD — return for public scene/boundary review',flush=True);break
    canon=re.sub('[^a-z0-9]','',low)
    same=same+1 if difflib.SequenceMatcher(None,canon,last).ratio()>.72 else 0;last=canon
    im=Image.open(STATE).convert('RGB');w,h=im.size
    box=im.crop((int(w*.08),int(h*.75),int(w*.90),int(h*.87)))
    textbox=sum(min(p)>235 and max(p)-min(p)<5 for p in box.getdata())/(box.width*box.height)>.55
    if same>=3 and textbox:act('c','wait:.4');same=0
    else:act('wait:.4')
else:raise SystemExit('Battle readiness timeout')
