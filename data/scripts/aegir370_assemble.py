"""Restore prepared reserves and arrange fixed Aegir party through normal PC UI."""
from play import *
def run(s,*a):
 print('AEGIR ASSEMBLE',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((ROOT/'notes/Aegir369-Supplies-status.json').read_text());assert s['map']==38
run('eventq',38,4,'talk');run('pc_open_reviewed');run('pc_select_box',3)
run('pc_exchange_named',15,3,'Amoonguss','Zapdos','--box',3,'--stay-open')
run('pc_select_box',2)
run('pc_exchange_named',25,4,'Mienshao','Arcanine','--box',2)
# Ray, Magearna, Heatran, Amoonguss, Mienshao, Cresselia
run('party_swap',0,2)
run('party_swap',1,5)
run('party_swap',2,5)
run('party_swap',3,4)
run('party_swap',4,5)
# Heatran, Cresselia, Magearna, Mienshao, Rayquaza, Amoonguss
run('eventq',38,3,'talk');run('heal');run('checkpoint','Aegir370-Assembled')
s=json.loads((ROOT/'notes/Aegir370-Assembled-status.json').read_text())
assert [p['species'] for p in s['party']]==['HEATRAN','CRESSELIA','MAGEARNA','MIENSHAO','RAYQUAZA','AMOONGUSS']
