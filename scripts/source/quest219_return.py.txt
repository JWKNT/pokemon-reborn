"""Return one inspected quest Pokemon using the ordinary name-verified party selector."""
from play import *
import argparse
p=argparse.ArgumentParser();p.add_argument('map',type=int);p.add_argument('event',type=int);p.add_argument('page',type=int);p.add_argument('name');a=p.parse_args()
source=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),str(a.map),str(a.event)],stderr=subprocess.DEVNULL))['pages'][a.page]['list']
s=' '.join(str(c['parameters']) for c in source)
assert 'pbChoosePokemon' in s and 'pbRemovePokemonAt' in s and 'pbTrainerBattle' not in s
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),str(a.map),str(a.event),'talk'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=35'])
t=read().lower();assert 'choose a pok' in t or ('cancel' in t and 'able' in t),t
subprocess.run([sys.executable,str(ROOT/'scripts/party_pick.py'),a.name,'--single'],check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/dialog.py'),'--limit=35'],check=True)
print('RETURN DIALOGUE FINISHED',a.name,flush=True)
