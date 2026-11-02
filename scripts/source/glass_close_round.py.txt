"""Close a won Glass battle at HUD disappearance, then open the next round.
Never save/reload between rounds, and never read an in-progress battle log.
"""
from play import *
import argparse
p=argparse.ArgumentParser();p.add_argument('major',type=int);p.add_argument('session',type=int);p.add_argument('--next',type=int,dest='next_major');p.add_argument('--baseline',required=True);a=p.parse_args()
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,args)],check=True)
music=json.loads((ROOT/'work/active-trainer-music.json').read_text());start=music['start_epoch']
assert any(x['epoch']>=start and re.search(r'de.?feated|for winning',' '.join(x['text']),re.I)for x in(json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()))
def hud(rows):
 own=' '.join(x['text']for x in rows if x['x']>.5 and .4<x['y']<.72)
 compact=re.sub('[^a-z]','',own.lower())
 return ('arcanine'in compact or 'klinklang'in compact)and bool(re.search(r'\bhp\b|l[uv][ .]*90',own,re.I))
for _ in range(30):
 rows=snap();t=' '.join(x['text']for x in rows);print(t,flush=True)
 assert not any(w in t.lower()for w in ['fight','choose a pok','trying to learn','switch in','out of usable']),'Unexpected battle input'
 if not hud(rows):
  act('wait:.7');assert not hud(snap()),'HUD still transitioning';break
 act('c','wait:.5')
else:raise SystemExit('Victory HUD closing limit')
run('major_attempt','victory',ROOT/f'work/major-{a.major}.json',a.session)
run('trainer_music','finish','--world-verified');run('sync_battle_logs')
if a.next_major:
 run('glass_continuity',ROOT/f'work/major-{a.next_major}.json',a.baseline)
 run('major_enter',ROOT/f'work/major-{a.next_major}.json',a.session,734,12,'--status',ROOT/f'notes/glass-{a.next_major}-round-entry-status.json','--continuity-proof',ROOT/f'work/glass-{a.next_major}-continuity.json','--active-dialogue')
print('GLASS ROUND CLOSED / NEXT COMMAND READY',read(),flush=True)
