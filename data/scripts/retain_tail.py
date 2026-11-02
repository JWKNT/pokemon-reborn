"""Retain automatic battle animation after an early UI guard stops issuing inputs."""
import json,pathlib,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
def retain(epoch=None,seconds=12):
 now=time.time() if epoch is None else epoch
 for p in sorted((ROOT/'recordings').glob('session-???.json'),reverse=True):
  m=json.loads(p.read_text())
  if m['start_epoch']<=now and 'stop_epoch' not in m:
   m.setdefault('include_intervals',[]).append([now-m['start_epoch'],now-m['start_epoch']+seconds]);p.write_text(json.dumps(m,indent=2));return
