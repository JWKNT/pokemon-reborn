"""Second, conservative edge check for stationary world scenes with cyclic lighting.

The original pixel validator intentionally rejects brightness animation. This
checks the full scene's edges (including the player and all NPCs), stops at any
change, and saves before/middle/after images for visual review.
"""
from pathlib import Path
import subprocess,json,numpy as np
from PIL import Image,ImageDraw
from validate_video_idle import edge,dil
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'work/idle-audit-2026-09-30'
for folder in sorted(WORK.iterdir()):
    p=folder/'validated.json'
    if not p.exists():continue
    j=json.loads(p.read_text());added=[]
    for c in j['rejected']:
        if c['mode']!='whole_loop' or c['class']!='field' or c['duration']<4:continue
        # Keep the beginning and stop before any changed world edge.
        a=int(np.ceil((c['start']+.6)*30));b=int(np.floor((c['end']-.4)*30));base=a-16
        vf='scale=320:240'
        raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-nostdin','-v','error','-threads','2','-reinit_filter','0','-ss',str(base/30),'-i',j['source']['path'],'-t',str((b-base)/30),'-vf',vf,'-pix_fmt','gray','-f','rawvideo','-'])
        n=len(raw)//76800;ims=np.frombuffer(raw[:n*76800],np.uint8).reshape(n,240,320)
        if n<32:continue
        ee=np.array([edge(im) for im in ims[:16]]);required=ee.all(0);allow=dil(ee.any(0));end=16
        for i in range(16,n):
            e=edge(ims[i]);diff=(e&~allow)|(required&~dil(e));tiles=diff.reshape(30,8,40,8).sum((1,3))
            if diff.mean()>.0015 or tiles.max()>10:break
            end=i+1
        b=min(b,base+end-9)
        if b-a<15:continue
        proof=Image.new('RGB',(960,270),(20,20,20));dr=ImageDraw.Draw(proof)
        for k,i in enumerate([15,(16+end)//2,max(16,end-10)]):
            proof.paste(Image.fromarray(ims[i]).convert('RGB'),(k*320,0));dr.text((k*320+4,245),f'{(base+i)/30:.3f}s',fill='white')
        path=folder/f'world-proof-{c["id"]}.jpg';proof.save(path,quality=90)
        added.append({**c,'a':a,'b':b,'validation':'full-scene edges: stationary player, NPCs and camera; animated brightness ignored','proof':str(path)})
    if added:
        # Visual review showed transitions in the baseline can hide input changes.
        # Keep these as proposals; never automatically merge them into the edit.
        j['world_loop_proposals']=added
        p.write_text(json.dumps(j,indent=2)+'\n')
        print(folder.name,'stationary-world proposals requiring visual review',len(added),flush=True)
