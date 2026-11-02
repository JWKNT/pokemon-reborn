"""Verified short-D quicksave; optional named backup and full read-only evidence."""
from play import *
import shutil,re,difflib
# User's hard-route League rule: the entire seven-fight chain has no saves.
league_guard=ROOT/'notes/active-league-chain.json'
if league_guard.exists():
 league=json.loads(league_guard.read_text())
 if league.get('status') in ['active','failed']:
  raise SystemExit('League no-save guard: complete the entire winning chain or restore its pre-entry save after a loss before saving')
savepath=pathlib.Path.home()/'Library/Application Support/Pokemon Reborn/Game_3.rxdata'
screen_before=read().lower()
if 'keyboard' in screen_before or 'what is it' in screen_before:
 raise SystemExit('Text-entry screen: finish the quest answer before saving')
before=savepath.stat().st_mtime
act('d:0.12','wait:1');t=read().lower()
# Hazard hit animations occasionally consume the initial short-D input.
# Only retry while the public screen is empty overworld, never a dialog.
for retry in range(3):
 if re.sub('[^a-z]','',t) not in ['', 'pokemonreborn']:break
 act('wait:.4','d:0.12','wait:1');t=read().lower()
compact=re.sub('[^a-z]','',t)
if not (re.search(r'\b(?:would|hould|wouid) you like to save',t) or ('yes' in compact and 'no' in compact and 'savethegame' in compact)):
 raise SystemExit('Quicksave prompt review: '+t)
act('c','wait:1');t=read().lower();print(t,flush=True)
if savepath.stat().st_mtime<=before:raise SystemExit('Save timestamp did not advance: '+t)
if 'saved the game' not in t and 'sawed the game' not in t:print('SAVE TIMESTAMP VERIFIED; fragmented confirmation OCR',flush=True)
act('c','wait:.6')
if savepath.stat().st_mtime<=before:raise SystemExit('Save timestamp did not advance')
subprocess.run(['ruby',str(ROOT/'scripts/sync_navigation.rb')],stderr=subprocess.DEVNULL,check=True)
if len(sys.argv)>1:
 name=sys.argv[1];assert name.replace('-','').replace('_','').isalnum()
 shutil.copy2(savepath,ROOT/'backups'/f'Aster-{name}.rxdata')
 raw=subprocess.check_output(['ruby',str(ROOT/'scripts/status_full.rb')],stderr=subprocess.DEVNULL)
 (ROOT/'notes'/f'{name}-status.json').write_bytes(raw)
 shutil.copy2(ROOT/'notes/navigation-state.json',ROOT/'notes'/f'{name}-navigation.json')
print('QUICKSAVE VERIFIED',time.time(),flush=True)
