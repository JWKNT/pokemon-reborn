from bgm_span import *
import sys,time,re
name=sys.argv[1].lower();rows=[json.loads(l) for l in (ROOT/'recordings/screens.jsonl').read_text().splitlines()];rows=[dict(r,low=' '.join(r['text']).lower()) for r in rows]
starts=[i for i,r in enumerate(rows) if name in r['low'] and ('angry' in r['low'] or 'appeared' in r['low'])]
if not starts:raise SystemExit('No encounter introduction')
i=starts[-1];r=rows[i:];start=r[0]['epoch']-2
faint=next((x['epoch'] for x in r if 'fainted' in x['low']),None)
if faint is None:raise SystemExit('No confirmed faint')
end=next((x['epoch'] for x in r if x['epoch']>faint and 'roars triumphantly' in x['low']),time.time())
append_span(start,faint,wild_track());append_span(faint,end,'Victory!');print(name,start,faint,end)
