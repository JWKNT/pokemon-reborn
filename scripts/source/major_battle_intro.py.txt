"""Anchor an open recorded major attempt at its observed battle introduction."""
import json,re,time,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];cfg=json.loads(pathlib.Path(sys.argv[1]).read_text());number=int(sys.argv[2])
p=ROOT/'recordings/major-fights'/f'session-{number:03}-attempts.json';rows=json.loads(p.read_text());row=rows[-1]
assert row['id']==cfg['id'] and 'end'not in row
norm=lambda s:re.sub('[^a-z]','',s.lower()).replace('amerthyst','amethyst').replace('meutuo','mewtwo').replace('meutwo','mewtwo')
name=norm(cfg.get('intro_name',cfg['opponent']));hits=[]
for line in(ROOT/'recordings/screens.jsonl').read_text().splitlines():
 s=json.loads(line);text=' '.join(s['text']);c=norm(text)
 if s['epoch']<row['battle_start_epoch'] or name not in c:continue
 custom = cfg.get('trainer_key')==['CHILDLIN','Lin',0] and cfg.get('intro_name')=='Arceus' and 'herepuppygogetem' in c and 'hp' in c
 if (cfg.get('intro_title_line') and norm(cfg['intro_title_line']) in [norm(z) for z in s['text']]) or custom or re.search(r'\bvs\b',text,re.I) or re.search('[wmuv]ouldliketobattle',c) or ('sentout' in c and name in c):hits.append(s)
assert hits,'Observed battle introduction required'
s=hits[0];meta=json.loads((ROOT/'recordings'/f'session-{number:03}.json').read_text());row['interaction_start_epoch']=row['battle_start_epoch'];row['battle_start_epoch']=s['epoch'];row['start']=s['epoch']-meta['start_epoch'];row['battle_intro_evidence']=s
p.write_text(json.dumps(rows,indent=2)+'\n')
a=ROOT/'work/active-trainer-music.json';m=json.loads(a.read_text());assert m['name']==cfg['opponent'];m['interaction_start_epoch']=m['start_epoch'];m['start_epoch']=s['epoch'];m['battle_intro_evidence']=s;a.write_text(json.dumps(m,indent=2)+'\n')
print('ACTUAL BATTLE INTRO VERIFIED',s['epoch'],s['text'],flush=True)
