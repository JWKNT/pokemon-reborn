"""Reconcile failed chase spans using black death fades in recorded pixels only."""
import json,subprocess,sys,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];n=int(sys.argv[1]);p=R/'recordings'/f'session-{n:03}.json';m=json.loads(p.read_text());rows=[];spans=[];evidence=[]
for f in sorted((R/'work').glob('amethyst-attempt-*/journal.json')):
 d=json.loads(f.read_text());st=d['start_epoch']
 if d.get('reviewed_outcome') and d['reviewed_outcome']!='failed':continue
 if st<m['start_epoch'] or st>m.get('stop_epoch',float('inf')) or not d.get('end_epoch') or d['end_epoch']>time.time():continue
 cue=next((x['epoch'] for x in d['events'] if x['kind']=='start_warning'),None)
 if not cue:continue
 a=cue-m['start_epoch']+2;length=min(60,d['end_epoch']-cue+3)
 raw=subprocess.check_output(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(a),'-i',str(R/m['raw']),'-t',str(length),'-vf','fps=10,scale=16:16','-pix_fmt','rgb24','-f','rawvideo','-'])
 pixels=np.frombuffer(raw,np.uint8).reshape(-1,16,16,3);means=pixels.mean(axis=(1,2,3));black=np.flatnonzero(means<3)
 if len(black):
  b=int(black[0]);after=np.flatnonzero(means[b:]>30)
  if len(after):
   end=a+(b+int(after[0]))/10+.5;music_end=a+b/10
   evidence.append({'journal':str(f.relative_to(R)),'black_fade_raw':music_end,'return_raw':end,'source':'Recorded RGB16 means at10fps; first black death fade then lit return; visually check contact sheet'})
  else:continue
 else:continue
 rows.append([st-m['start_epoch'],end]);spans.extend([{'start':cue-m['start_epoch'],'end':music_end,'track':'Battle- Misc','reason':'Recorded chase warning to death fade'},{'start':music_end,'end':end,'track':'Atmosphere- Triumph','reason':'Death transition back to Amethyst entry'}])
if '--apply' in sys.argv:
 existing=m.get('include_intervals',[]);starts={round(s,2) for s,e in rows};m['include_intervals']=[(s,e)for s,e in existing if round(s,2)not in starts]+rows;p.write_text(json.dumps(m,indent=2))
 out=R/'work'/f'session-{n:03}-music-overrides.json';old=json.loads(out.read_text())if out.exists()else[];cue_starts={round(x['start'],2) for x in spans};old=[x for x in old if not (x.get('reason','').startswith(('Public Amethyst','Recorded chase','Death transition')) and round(x['start'],2) in cue_starts)];out.write_text(json.dumps(old+spans,indent=2))
(R/'notes'/f'session{n}-chase-boundaries.json').write_text(json.dumps(evidence,indent=2));print('FAILED CHASES RECONCILED',len(rows))
