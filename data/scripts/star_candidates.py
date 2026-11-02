"""Offline Mastermind planning from publicly observed yellow/white feedback only."""
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
p=Path(sys.argv[1]);history=json.loads(p.read_text()) if p.exists() else []
allc=np.array([a for a in itertools.product(range(1,5),repeat=7)if max(Counter(a).values())<=3],dtype=np.int8)
a=allc.copy()
def counts(a):return np.array([(a==v).sum(axis=1)for v in range(1,5)]).T
for h in history:
 g=np.array(h['guess']);gold=np.minimum(counts(a),counts(g[None,:])[0]).sum(axis=1);white=(a==g).sum(axis=1)
 a=a[(gold==h['yellow'])&(white==h['white'])]
assert len(a),'Inconsistent public feedback; review before further input'
if not history:guess=[1,1,1,2,2,3,4]
elif len(a)==1:guess=a[0].tolist()
else:
 rng=np.random.default_rng(215);pool=allc if len(a)<=64 else (a if len(a)<=256 else a[rng.choice(len(a),256,replace=False)])
 ac=counts(a);last=np.array(history[-1]['guess']);best=None
 for g in pool:
  gold=np.minimum(ac,counts(g[None,:])[0]).sum(axis=1);white=(a==g).sum(axis=1);freq=np.bincount(gold*8+white,minlength=64)
  score=(int((freq*freq).sum()),int((g!=last).sum()),tuple(g))
  if best is None or score<best:best=score;guess=g.tolist()
print(json.dumps({'remaining':len(a),'next_guess':guess,'public_guesses':len(history)}))
