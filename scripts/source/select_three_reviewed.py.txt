"""Choose three reviewed owned members in the normal entry screen; stop before Confirm."""
from play import *
import argparse,shutil
p=argparse.ArgumentParser();p.add_argument('order');p.add_argument('evidence');a=p.parse_args();order=a.order.split('|');assert len(order)==len(set(order))==3
r=read();compact=re.sub('[^a-z]','',r.lower().replace('é','e'));assert 'choosepokemonandconfirm' in compact and 'notentered' in compact,('Fresh challenge selection required',r)
for name in order:
 subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),name,'--single'],check=True)
 t=read().lower();assert 'entry' in t and 'summary' in t and 'cancel' in t and 'no entry' not in t,('Unselected member entry menu required',t)
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Entry|Summary|Cancel','Entry'],check=True)
# The blinking Confirm highlight can briefly corrupt a neighboring ordinal in OCR.
# Observe up to three fresh frames; never alter the selection to repair OCR.
for observation in range(3):
 t=read();compact=re.sub('[^a-z]','',t.lower())
 if all(w in compact for w in ['first','second','third','confirm']):break
 if observation<2:act('wait:.25')
else:raise AssertionError(('Review selected ordinals before entering',t))
p=pathlib.Path(a.evidence);assert not p.exists();shutil.copyfile(NATIVE,p)
p.with_suffix('.json').write_text(json.dumps(dict(order=order,epoch=time.time(),public_text=t,requires_visual_confirmation=True),indent=2)+'\n')
print('THREE SELECTED; STOPPED BEFORE CONFIRM',order,p,flush=True)
