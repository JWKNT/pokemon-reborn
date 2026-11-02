"""Use the normal trainer forfeit once to unlock Endgame's intended PC fallback."""
from play import *
t=read().lower()
if '--at-choice' not in sys.argv and '--after-choice' not in sys.argv:
 assert 'fight' in t and 'run' in t, 'Battle command required'
 act('right:.2','down:.2','c','wait:.5')
t=read();print(t,flush=True)
if '--after-choice' not in sys.argv:
 assert 'forfeit' in re.sub('[^a-z]','',t.lower()), 'Expected normal forfeit confirmation'
 subprocess.run([sys.executable,str(ROOT/'scripts/choose_dialog.py'),'Yes|No','Yes'],check=True)
blank=0
for _ in range(40):
 t=read();print(t,flush=True);low=t.lower()
 if re.sub('[^a-z]','',low) in ['', 'pokemonreborn']:
  blank+=1
  if blank>=3:break
  act('wait:.7');continue
 blank=0
 assert not ('fight' in low or 'choose a pok' in low), 'Unexpected battle input'
 assert any(z in low for z in ['forfeited','out of usable','lost against','paid','prize money','blacked out','scurried','exhausted','fainted pok']) or re.sub('[^a-z]','',low)=='pokemonreborn', 'Loss dialogue review: '+t
 act('c','wait:.6')
else:raise SystemExit('Loss transition limit')
print('NORMAL FORFEIT COMPLETE; WORLD OBSERVED',flush=True)
