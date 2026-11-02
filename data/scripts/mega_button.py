"""Classify the public Mega button from a freshly recorded game-only frame.

Installed UI asset/placement are static references; no battle runtime reads.
Refuses unrecognized pixels instead of blindly toggling an unavailable button.
"""
from PIL import Image
from pathlib import Path

def classify(frame):
    asset=Image.open('/Applications/Reborn.app/Contents/Game/Graphics/Pictures/Battle/battleMegaEvo.png').convert('RGBA')
    assert asset.size==(96,92)
    variants=[asset.crop((0,y,96,y+46)) for y in (0,46)]
    # Focus on opaque pixels which distinguish grey and colored toggle states.
    a,b=[list(v.getdata()) for v in variants]
    mask=[i for i,(p,q) in enumerate(zip(a,b)) if p[3]>240 and q[3]>240 and sum(abs(p[j]-q[j]) for j in range(3))>100]
    assert len(mask)>30
    frame=Image.open(frame).convert('RGB');w,h=frame.size
    assert (w,h)==(852,640)
    crop=frame.crop((round(146*w/512),round(242*h/384),round(242*w/512),round(288*h/384))).resize((96,46),Image.Resampling.NEAREST)
    observed=list(crop.getdata())
    errors=[sum(abs(observed[i][j]-ref[i][j]) for i in mask for j in range(3))/(len(mask)*3) for ref in (a,b)]
    best=min(range(2),key=lambda i:errors[i])
    assert errors[best]<45 and errors[1-best]-errors[best]>12,('Mega button needs visual review',errors)
    return best+1,errors

def enable():
    from play import ROOT,act,snap
    import json,time
    snap();before,errors=classify(ROOT/'recordings/capture-preview.png')
    if before==1:
        act('a:.12','wait:.3');snap()
    after,after_errors=classify(ROOT/'recordings/capture-preview.png')
    assert after==2,('Mega toggle not active',after_errors)
    with (ROOT/'recordings/mega-ui.jsonl').open('a') as f:
        f.write(json.dumps({'epoch':time.time(),'before':before,'after':after,'errors_before':errors,'errors_after':after_errors,'source':'public capture and installed UI template'})+'\n')
    print('MEGA TOGGLE VISUALLY VERIFIED',flush=True)
