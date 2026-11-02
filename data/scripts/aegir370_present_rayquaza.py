"""Present the owned Rayquaza and decline optional PC; stop before battle scene."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('aegir_event',850,130,'talk')
for _ in range(8):
 t=read();print(t,flush=True);low=t.lower()
 if 'choose a pok' in low or ('cancel' in low and ('able' in low or low.count('hp')>=5)):break
 assert any(w in low for w in ['florinia','successful','procuring','neutralizing','energies','returned']),t
 act('c','wait:.5')
else:raise SystemExit('Rayquaza selection not reached')
run('party_pick','Rayquaza','--single')
# choose_dialog only accepts the source-reviewed Yes/No choice, without advancing battle.
run('choose_dialog','Yes|No','No','--source',850,130)
print('OPTIONAL PC DECLINED; review before battle entry',read(),flush=True)
