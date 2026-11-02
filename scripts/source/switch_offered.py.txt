"""Choose a free replacement only after a recent observed incoming opponent."""
from play import *
import difflib
foe,own=sys.argv[1:3]
t=read().lower()
assert 'change pok' in t or 'switch your' in t, 'Expected free replacement offer'
rows=[json.loads(l)for l in(ROOT/'recordings/screens.jsonl').read_text().splitlines()]
offers=[r for r in rows if time.time()-r['epoch']<90 and 'about to send' in ' '.join(r['text']).lower()]
assert offers, 'Incoming opponent announcement was not observed'
compact=lambda s:re.sub('[^a-z]','',s.lower())
announcement=compact(' '.join(offers[-1]['text']))
tail=announcement.split('abouttosendin')[-1]
assert compact(foe) in tail or difflib.SequenceMatcher(None,compact(foe),tail).ratio()>=.78, 'Different incoming opponent: '+str(offers[-1])
subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),own],check=True)
