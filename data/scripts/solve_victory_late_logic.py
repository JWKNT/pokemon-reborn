"""Solve only public written clues and left-to-right plaque ranks, not stored answers."""
import itertools,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=list(itertools.permutations(range(1,5)));out3=[];out4=[]
for s in P:
 if not(s[0]>s[1] and s[3]!=1):continue
 for p in P:
  if not p[1]<p[0]<p[3]:continue
  for f in P:
   if not(f[0]<f[1] and f[3]==4 and s[f.index(2)]<s[2] and p[f.index(1)]==1):continue
   for l in P:
    if not(l[3]!=2 and l[0]>l[3]>l[1] and l[s.index(4)]>l[s.index(1)]):continue
    gems=[s.index(3),p.index(2),f.index(1),l.index(3)]
    if len(set(gems))!=4:continue
    h=[0]*4
    for rank,g in enumerate(gems,1):h[g]=rank
    out3.append(dict(size=s,hardness=h,purity=p,foliation=f,luster=l))
for p in P:
 for l in P:
  if not p[l.index(2)]<p[2]<p[l.index(3)]:continue
  for f in P:
   if not f[l.index(3)]<f[l.index(2)]<f[l.index(1)]:continue
   for s in P:
    if not(s[p.index(1)]<s[f.index(3)]<s[1] and l[p.index(2)]<l[s.index(3)] and l[s.index(1)]<l[s.index(3)]):continue
    for h in P:
     if not(h[s.index(2)]<h[3]<h[p.index(3)] and f[3]<f[h.index(3)]<f[1]):continue
     for a in P:
      if a[h.index(3)]<a[p.index(3)]<a[2] and l[s.index(1)]<l[s.index(3)]<l[a.index(2)] and a[l.index(1)]<a[p.index(4)]:
       out4.append(dict(size=s,hardness=h,purity=p,foliation=f,luster=l,habit=a))
for number,out in [(3,out3),(4,out4)]:
 assert len(out)==1,(number,len(out))
 report=dict(basis='Public walkthrough clues, cross-checked plaque rank labels from installed map793/795 dialogue. No hidden answer or runtime state read.',rows=['Ruby','Sapphire','Emerald','Amethyst'],ranks=dict(size=['Miniscule','Small','Medium','Large'],hardness=[5,6,7,8],purity=['Impure','Middling','Pure','Flawless'],foliation=['Indistinct','Difficult','Perfect','Eminent'],luster=['Silky','Vitreous','Pearly','Adamantine'],habit=['Cubic','Hexagonal','Tabular','Coxcomb']),solutions=out)
 (R/f'work/198-gem-puzzle{number}-solution.json').write_text(json.dumps(report,indent=2)+'\n');print(number,out)
