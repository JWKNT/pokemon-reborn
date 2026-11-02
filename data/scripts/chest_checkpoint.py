"""Normal in-game save between defense battles, then restore the actual Bag pause.
The user explicitly authorized intermediate saves/reloads on October 5.
"""
from play import *
from chest_safe_pause import classify
from hashlib import sha256
name=sys.argv[1];assert name.replace('-','').isalnum()
if '--prompt-open' not in sys.argv:assert classify(snap())=='bag','Start from actual Bag'
savepath=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
before=savepath.stat().st_mtime
if '--prompt-open' not in sys.argv:act('x:.12','wait:1','x:.12','d:.12','wait:.5')
r=snap();t=' '.join(x['text']for x in r).lower()
assert 'would you like to save the game' in t,'Normal save permission prompt required: '+t
act('c:.12','wait:.7');r=snap();assert savepath.stat().st_mtime>before,'Native save did not advance'
act('c:.12','wait:.3','x:.12','wait:.3','c:.12','wait:1.2')
r=snap();assert classify(r)=='bag','Saved but Bag re-entry requires immediate review'
shutil.copy2(savepath,ROOT/'backups'/f'Aster-{name}.rxdata')
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status_full.rb')],stderr=subprocess.DEVNULL)
(ROOT/'notes'/f'{name}-status.json').write_bytes(raw)
subprocess.run(['ruby',str(ROOT/'scripts/sync_navigation.rb')],stderr=subprocess.DEVNULL,check=True)
shutil.copy2(ROOT/'notes/navigation-state.json',ROOT/'notes'/f'{name}-navigation.json')
# The snapshot is owned party/bag/player data, never active battle internals.
c=json.loads((ROOT/'notes/current-run-control.json').read_text());p=ROOT/c['active_gauntlet_journal'];j=json.loads(p.read_text());j.setdefault('checkpoints',[]).append({'label':name,'epoch':time.time(),'native_sha256':sha256(savepath.read_bytes()).hexdigest(),'completed_waves':[w['wave']for w in j['waves']],'authorization':'notes/user-save-reload-steer-2026-10-05.md'});p.write_text(json.dumps(j,indent=2));c['native_checkpoint']=name;(ROOT/'notes/current-run-control.json').write_text(json.dumps(c,indent=2))
print('NORMAL INTERMEDIATE SAVE VERIFIED; BAG PAUSED',name,flush=True)
