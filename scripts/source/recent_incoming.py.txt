"""Recover a missed visible switch announcement from the active screen recording."""
import pathlib,json,time,subprocess,re,difflib,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
def recent_incoming(since,names):
 rows=[json.loads(l)for l in (R/'recordings/screens.jsonl').read_text().splitlines()[-220:]]
 offers=[v for v in rows if v['epoch']>=since and any(z in ' '.join(v['text']).lower()for z in ['change pok','switch your'])]
 assert offers,'No observed free switch offer'
 first=offers[-1]['epoch']
 # Find the beginning of this same offer, not an older fight/earlier knockout.
 for v in reversed(rows):
  if v['epoch']<since:break
  if any(z in ' '.join(v['text']).lower()for z in ['change pok','switch your']):first=v['epoch']
  else:break
 metas=[json.loads(p.read_text())for p in (R/'recordings').glob('session-???.json')]
 meta=max((v for v in metas if v['start_epoch']<=first and ('stop_epoch'not in v or v['stop_epoch']>=first)),key=lambda v:v['start_epoch'])
 start=max(0,first-meta['start_epoch']-7)
 dest=R/'work/recent-announcement';dest.mkdir(exist_ok=True)
 for p in dest.glob('frame-*.png'):p.unlink()
 subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-ss',str(start),'-i',str(R/meta['raw']),'-t','8','-vf','fps=4,crop=iw:ih*.24:0:ih*.72,scale=1024:-1','-frames:v','32',str(dest/'frame-%03d.png')],check=True)
 seen=set();found=[]
 for p in sorted(dest.glob('frame-*.png')):
  sha=hashlib.sha256(p.read_bytes()).hexdigest()
  if sha in seen:continue
  seen.add(sha)
  text=' '.join(v['text']for v in json.loads(subprocess.check_output([str(R/'scripts/observe'),str(p)])))
  norm=re.sub('[^a-z]','',text.lower())
  if 'sendin' not in norm:continue
  tail=re.split('send\\s*in',text.lower())[-1]
  hits=[n for n in names if any(difflib.SequenceMatcher(None,n.lower(),w.strip('.,')).ratio()>=.78 for w in tail.split())]
  if len(hits)==1:found.append({'name':hits[0],'text':text,'frame':str(p),'source':'visible screen-recording replay'})
 assert found,'Announcement absent from recent recorded frames; manual review needed'
 result=found[-1]
 with(R/'recordings/announcement-replays.jsonl').open('a')as f:f.write(json.dumps(dict(result,epoch=time.time(),offer_epoch=first,raw=meta['raw'],offset=start))+'\n')
 return result['name']
if __name__=='__main__':import sys;print(recent_incoming(float(sys.argv[1]),sys.argv[2].split(',')))
