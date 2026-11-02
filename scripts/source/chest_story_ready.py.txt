"""Advance reviewed Saphira instructions, stopping before the speed-up warning."""
from play import *
for _ in range(35):
 t=read();print(t,flush=True);lo=t.lower()
 if 'speed-up' in lo or 'speed up' in lo or 'suggested' in lo:break
 if any(r['text'].strip().lower() in ['yes','no','happiness','money','friends','hp'] for r in snap()):raise SystemExit('Choice/battle review')
 if not any(len(r['text'])>3 and r['y']>.72 for r in snap()):raise SystemExit('No dialogue')
 act('c:.12','wait:.35')
