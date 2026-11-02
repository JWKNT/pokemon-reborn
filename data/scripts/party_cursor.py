"""Observe the party selection border before navigating the six-card grid."""
from collections import deque
from PIL import Image

def selected_card(path):
    im=Image.open(path).convert('RGB');w,h=im.size;scores=[]
    # Sample the straight vertical outline, avoiding the previous card's bottom
    # edge. The broad x search tolerates native window-shadow/title-bar variants.
    for slot in range(6):
        col=slot%2;row=slot//2
        left,right=(.025,.080) if not col else (.505,.550)
        top=(.145 if not col else .180)+.211*row
        xs=range(int(w*left),int(w*right));ys=range(int(h*top),int(h*(top+.080)))
        score=max(sum(min(im.getpixel((x,y)))>210 and max(im.getpixel((x,y)))-min(im.getpixel((x,y)))<20 for y in ys)/len(ys) for x in xs)
        scores.append(score)
    ranked=sorted(range(6),key=lambda x:scores[x],reverse=True)
    if scores[ranked[0]]<.75 or scores[ranked[0]]-scores[ranked[1]]<.3:raise RuntimeError(f'Party selection border review: {scores}')
    return ranked[0]

def selection_path(start,target,multiselect=False):
    # Installed Party.rb: horizontal navigation is linear and wraps via Cancel.
    count=8 if multiselect else 7
    q=deque([(start,[])]);seen={start}
    while q:
        slot,keys=q.popleft()
        if slot==target:return keys
        up=count-1 if slot<2 else (slot-2 if slot<6 else slot-1)
        for key,nxt in [('right',(slot+1)%count),('left',(slot-1)%count),('up',up),('down',slot+2 if slot<5 else (slot+1)%count)]:
            if nxt not in seen:seen.add(nxt);q.append((nxt,keys+[key+':0.12']))
    raise RuntimeError('Party navigation route unavailable')
