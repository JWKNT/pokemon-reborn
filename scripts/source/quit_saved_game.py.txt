"""Verify an already closed macOS game and back up its save; sends no quit key."""
# This helper deliberately leaves the quitting keystroke to the CUA app binding.
# Read-only verification and backup are performed after the app closes.
from play import *
import shutil
label=sys.argv[1]
assert label.replace('-','').replace('_','').isalnum()
processes=subprocess.check_output(['ps','-axo','command='],text=True).splitlines()
assert not any(line.strip().startswith('/Applications/Reborn.app/') for line in processes),'Reborn is still running; quit normally before this helper'
p=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status_full.rb')],stderr=subprocess.DEVNULL)
j=json.loads(raw);assert j['trainer']['name']=='Aster' and isinstance(j['trainer']['badges'],list)
(ROOT/'notes'/f'{label}-quit-status.json').write_bytes(raw)
shutil.copy2(p,ROOT/'backups'/f'Aster-{label}-quit.rxdata')
print('POST-QUIT SAVE BACKUP',j['save_mtime'],j['map'],j['position'],flush=True)
