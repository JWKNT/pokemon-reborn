"""Sync a verified milestone to the private project; no game input, no publishing."""
from pathlib import Path
import json,shutil,subprocess,hashlib,sys,re,datetime
from handoff_context import endpoint, journey_verification, resume_text
R=Path(__file__).resolve().parents[1];D=Path('/Users/jw/Desktop/bin/reborn');name=sys.argv[1];capture=int(sys.argv[2]);closed='--quit' in sys.argv
S=R/'notes'/f'{name}-status.json';s=json.loads(S.read_text());native=Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata';backup=R/'backups'/f'Aster-{name}.rxdata';assert native.read_bytes()==backup.read_bytes()
sha=hashlib.sha256(native.read_bytes()).hexdigest();nav=json.loads((R/'notes'/f'{name}-navigation.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat();badges=s['trainer']['badges'].count(True)
control=json.loads((R/'notes/current-run-control.json').read_text())
active_status=endpoint(control,closed)
meta=json.loads((R/'recordings'/f'session-{capture:03d}.json').read_text())
gym,gp,g=journey_verification(R,meta)
v=json.loads((R/'recordings/major-fights/verification.json').read_text())
master=json.loads((R/'recordings/major-fights/manifest.json').read_text())
resume=resume_text(root=R,name=name,save=s,navigation=nav,sha=sha,capture=capture,
                   metadata=meta,journey=g,master=master,verification=v,
                   control=control,closed=closed,now=now)
postgame_path=R/'recordings/postgame-major-fights/manifest.json'
if postgame_path.exists():
 pm=json.loads(postgame_path.read_text())
 if pm.get('published_count'):
  resume += f"\nPostgame major victories are published separately: {pm['published_count']} chapter(s), `{Path(pm['output']).name}`, SHA256 `{pm['published_sha256']}`. The original main-story master is complete and ends at major142.\n"
(R/'notes/RESUME.md').write_text(resume)
(R/'RESUME.md').write_text(resume)
# The active workspace has the same canonical paths named in its resume.
# Keep them current alongside the Desktop transfer package.
(R/'saves/current').mkdir(parents=True,exist_ok=True)
shutil.copy2(backup,R/'saves/current/Game_3.rxdata')
(R/'handoff').mkdir(exist_ok=True)
shutil.copy2(S,R/'handoff/save-state.json')
exts={'.py','.rb','.swift','.sh','.json','.jsonl','.md','.txt','.html','.filter','.ffmetadata','.ffconcat','.err','.rxdata'}
for dr in ('scripts','notes','work','recordings','backups','saves'):
 for p in (R/dr).rglob('*'):
  if not p.is_file()or p.is_symlink()or '__pycache__'in p.parts or p.suffix.lower()not in exts or (p.name.startswith('active-') and p.name!='active-league-chain.json'):continue
  q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True)
  if not q.exists()or q.read_bytes()!=p.read_bytes():shutil.copy2(p,q)
shutil.copy2(backup,D/'saves/current/Game_3.rxdata');shutil.copy2(S,D/'handoff/save-state.json');(D/'RESUME.md').write_text(resume)
p=D/'docs/DOT_HANDOFF.md';t=p.read_text();a=t.index('The current Mac run') if 'The current Mac run' in t else t.index('The user continued on the original Mac');b=t.index('\n## Read in this order',a);t=t[:a]+f'The current Mac run is summarized in RESUME.md. Latest native checkpoint is {name}, {badges} badges, map{s["map"]}{s["position"]}. '+active_status+' A later Linux transfer still requires recorded compatibility/input/capture validation.\n'+t[b:]
a=re.search(r'^## (?:Historical Ciel[^\n]*|Verified game state)',t,re.M).start();b=t.index('## Initial Linux VM setup',a);t=t[:a]+'## Verified game state\n\nRead RESUME.md and handoff/save-state.json for the current canonical native state. These supersede all historical Ciel/Fiore locations and builds below. Preserve the canonical copy and verify its hash before loading a transfer.\n\n'+t[b:];t=re.sub(r'Confirm Aster,13 badges, Agate Circus357\[4,9\], and the injured party match the current snapshot\.',f'Confirm Aster, {badges} badges, map{s["map"]}{s["position"]}, and the exact current party from handoff/save-state.json.',t);p.write_text(t)
p=D/'docs/LINUX_SETUP.md';t=p.read_text();t=re.sub(r'SHA256 [a-f0-9]{64}',f'SHA256 {sha}',t);a=t.index('It matches');b=t.index('\nDiscover the Linux',a);t=t[:a]+f'It matches native checkpoint {name}: Aster, {badges} badges, map{s["map"]}{s["position"]}, HARDCAP only. Read current RESUME and exact handoff/save-state.json; historical Ciel location/party is superseded.\n'+t[b:];t=re.sub(r'Session096 is the next unused recording number in this handoff;',f'Session{capture} is the current local recording number; the next unused number is at least {capture+1};',t);p.write_text(t)
p=D/'tools/preflight.py';t=p.read_text();t=re.sub(r'EXPECTED_SAVE_SHA256 = "[a-f0-9]+"',f'EXPECTED_SAVE_SHA256 = "{sha}"',t);p.write_text(t)
p=D/'handoff/media-catalog.json';cat=json.loads(p.read_text());f=Path(g['desktop']);row={'filename':f.name,'bytes':f.stat().st_size,'sha256':g['sha256'],'frames':g['frames'],'duration':g['duration']};cat['files']=[x for x in cat['files']if x.get('filename') not in [f.name, f'gym-{gym:02}-progress-game-4x-bgm.mp4' if g.get('milestone_complete') else f.name]]+[row];cat['updated']=now;p.write_text(json.dumps(cat,indent=2)+'\n')
# Keep the major media row current as well as the journey row.
cat=json.loads((D/'handoff/media-catalog.json').read_text());mf=Path(master['output'])
assert mf.stat().st_size==v['bytes'] and master['published_sha256']==v['sha256']
cat['files']=[x for x in cat['files']if x.get('filename')!=mf.name]+[{'filename':mf.name,'bytes':v['bytes'],'sha256':v['sha256'],'frames':v['frames'],'duration':v['duration']}]
(D/'handoff/media-catalog.json').write_text(json.dumps(cat,indent=2)+'\n')
# A capture can span a level-cap boundary. Catalog both verified journey parts.
segment_registry=R/'recordings'/f'session-{capture:03}-journey-segments.json'
if segment_registry.exists():
 for segment in json.loads(segment_registry.read_text())['segments']:
  evidence=json.loads((R/'notes'/f"gym{segment['gym']}-progress-verification.json").read_text())
  media=Path(evidence['desktop'])
  assert media.stat().st_size==evidence['bytes']
  cat['files']=[x for x in cat['files'] if x.get('filename')!=media.name]+[{'filename':media.name,**{k:evidence[k] for k in ['bytes','sha256','frames','duration']}}]
postgame_manifest=R/'recordings/postgame-major-fights/manifest.json'
if postgame_manifest.exists():
 pm=json.loads(postgame_manifest.read_text())
 if pm.get('published_count'):
  pv=json.loads(postgame_manifest.with_name('verification.json').read_text());media=Path(pm['output'])
  assert pm['published_sha256']==pv['sha256'] and media.stat().st_size==pv['bytes']
  cat['files']=[x for x in cat['files'] if x.get('filename')!=media.name]+[{'filename':media.name,**{k:pv[k] for k in ['bytes','sha256','frames','duration']}}]
(D/'handoff/media-catalog.json').write_text(json.dumps(cat,indent=2)+'\n')
# Build once after all package edits; preflight output stays outside the manifest.
subprocess.run([sys.executable,str(R/'scripts/refresh_handoff_docs.py'),name,str(capture)]+(['--quit']if closed else []),check=True)
rels=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=D,text=True).splitlines();files=[]
for rel in sorted(set(rels)):
 p=D/rel
 if not p.is_file()or p.is_symlink()or rel=='handoff/package-manifest.json':continue
 with p.open('rb')as z:h=hashlib.file_digest(z,'sha256').hexdigest()
 files.append({'path':rel,'bytes':p.stat().st_size,'sha256':h})
(D/'handoff/package-manifest.json').write_text(json.dumps({'scope':'Current Git-eligible package files except this self-referential manifest. External MP4s have separate media-catalog hashes.','updated':now,'file_count':len(files),'bytes':sum(x['bytes']for x in files),'files':files},indent=2)+'\n')
with (R/'work/latest-handoff-preflight.json').open('w')as out:subprocess.run([sys.executable,str(D/'tools/preflight.py'),'--game-dir','/Applications/Reborn.app/Contents/Game','--json'],stdout=out,check=True)
print('SYNC VERIFIED',name,'save',sha,'files',len(files),'game closed',closed)
