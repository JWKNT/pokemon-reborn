"""Prepare reviewed reusable moves, item and Chess piece order through normal UI."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(s,*a):
 print('CASTLE PREP',s,*a,flush=True);subprocess.run([sys.executable,str(R/'scripts'/f'{s}.py'),*map(str,a)],check=True)
s=json.loads((R/'notes/Postgame259-FireTeam-Cap120-status.json').read_text());assert all(m['level']==120 for m in s['party'])
run('teach_machine','TM92','Cresselia','Trick Room',2,'--single-step')
run('teach_machine','TM75','Mawile','Swords Dance',3,'--single-step')
run('give_held','Charcoal','Arcanine','--single-step')
run('party_front','Swampert','Zapdos','Mawile','Arcanine','Aegislash','Cresselia')
run('checkpoint','Postgame259-CastleBuild')
s=json.loads((R/'notes/Postgame259-CastleBuild-status.json').read_text())
assert [m['name'] for m in s['party']]==['Swampert','Zapdos','Mawile','Arcanine','Aegislash','Cresselia']
by={m['name']:m for m in s['party']};assert by['Arcanine']['item']=='CHARCOAL' and by['Cresselia']['moves'][2]['move']=='TRICKROOM' and by['Mawile']['moves'][3]['move']=='SWORDSDANCE'
print('CASTLE BUILD VERIFIED',flush=True)
