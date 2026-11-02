"""Read-only pixel-template correction for the native coordinate popup digits."""
import json,pathlib
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
def fix_coordinates(path,old,cropped=False):
 templates=json.loads((ROOT/'work/coordinate-digit-templates.json').read_text())['templates']
 im=Image.open(path).convert('RGB');w,h=im.size
 if not cropped:im=im.crop((int(w*.09),int(h*.75),int(w*.91),int(h*.86)))
 w,h=im.size
 hh=round(h*.525);ww=min(w,round(w*.92));cols=[sum(max(im.getpixel((x,y)))<150 for y in range(hh))>=5 for x in range(ww)]
 runs=[];i=0
 while i<len(cols):
  if not cols[i]:i+=1;continue
  a=i
  while i<len(cols)and cols[i]:i+=1
  runs.append((a,i))
 if len(runs)<12:return old
 widths=sorted(b-a for a,b in runs[:14]);typical=widths[len(widths)//2]
 commas=[i for i,(a,b)in enumerate(runs)if b-a<typical*.5][:3]
 if len(commas)!=3:return old
 groups=[runs[1:commas[0]],runs[commas[0]+2:commas[1]],runs[commas[1]+4:commas[2]]]
 if not all(1<=len(g)<=3 for g in groups):return old
 result=[]
 for g,number in zip(groups,old):
  digits=[];original=str(number)
  for index,(a,b)in enumerate(g):
   pts=[(x,y)for x in range(a,b)for y in range(hh)if max(im.getpixel((x,y)))<150]
   if not pts:return old
   x0,y0=min(x for x,y in pts),min(y for x,y in pts);x1,y1=max(x for x,y in pts)+1,max(y for x,y in pts)+1
   mask=Image.new('L',(x1-x0,y1-y0));mask.putdata([255 if max(im.getpixel((x,y)))<150 else 0 for y in range(y0,y1)for x in range(x0,x1)]);mask=mask.resize((10,20),Image.Resampling.NEAREST)
   sig=''.join('1'if z else'0'for z in mask.getdata());scores=sorted((sum(a!=b for a,b in zip(sig,s))/200,k)for k,s in templates.items())
   if scores[0][0]<=.01 and (len(scores)<2 or scores[1][0]>.04):digits.append(scores[0][1])
   elif len(g)==len(original):digits.append(original[index])
   else:return old
  result.append(int(''.join(digits)))
 return tuple(result)
