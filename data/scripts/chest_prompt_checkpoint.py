"""Normal D quicksave, retaining the game's Saved message (Mid_quicksave locks routes)."""
from play import *
from hashlib import sha256
name=sys.argv[1];assert name.replace('-','').isalnum()
p=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata';before=p.stat().st_mtime
act('d:.12','wait:.35')
t=read().lower();assert 'would you like to save the game' in t,t
act('c:.12','wait:.6')
t=read().lower();assert 'saved the game' in t and p.stat().st_mtime>before,t
shutil.copy2(p,ROOT/'backups'/f'Aster-{name}.rxdata')
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status_full.rb')],stderr=subprocess.DEVNULL);(ROOT/'notes'/f'{name}-status.json').write_bytes(raw)
subprocess.run(['ruby',str(ROOT/'scripts/sync_navigation.rb')],stderr=subprocess.DEVNULL,check=True)
shutil.copy2(ROOT/'notes/navigation-state.json',ROOT/'notes'/f'{name}-navigation.json')
navigation=json.loads((ROOT/'notes/navigation-state.json').read_text())
assert navigation['switches'].get('1074') and navigation['variables'].get('478',0)>0, 'Normal save preserved, but defense inactive; do not promote as retained victory'
assert navigation['variables'].get('479',5)<5, 'Chest failure pending; checkpoint requires review'
c=json.loads((ROOT/'notes/current-run-control.json').read_text());c.update(native_checkpoint=name,canonical_native_sha256=sha256(p.read_bytes()).hexdigest(),next_action='Saved message remains open; inspect current checkpoint and intercept the next remaining wave.')
(ROOT/'notes/current-run-control.json').write_text(json.dumps(c,indent=2))
jp=ROOT/c['active_gauntlet_journal'];j=json.loads(jp.read_text());j.setdefault('checkpoints',[]).append({'label':name,'epoch':time.time(),'native_sha256':c['canonical_native_sha256'],'method':'Normal D quicksave; Saved message left open; game-native Mid_quicksave freezes enemy routes'});jp.write_text(json.dumps(j,indent=2))
print('NORMAL QUICK SAVE VERIFIED; SAVED MESSAGE REMAINS OPEN',name,flush=True)
