"""Close reviewed completed pair, move to next fixed mountain pair, and stop in battle."""
from play import *
import argparse
p=argparse.ArgumentParser();p.add_argument('finished',type=int);p.add_argument('next',type=int);p.add_argument('lead',type=int);p.add_argument('names');a=p.parse_args()
assert (a.finished,a.next) in [(124,130),(130,152)]
def run(s,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/s),*map(str,args)],check=True)
run('trainer_music.py','finish')
run('linear_dialog.py',439,a.finished,'--active','--past-battle','--burst')
state_path=ROOT/'notes/navigation-state.json'
state=json.loads(state_path.read_text());state['variables']['193']={124:25,130:26}[a.finished];state_path.write_text(json.dumps(state))
run('party_lead.py',a.lead)
run('trainer_music.py','start','MeteorAceM',a.names)
e=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/event_dump.rb'),'439',str(a.next)],stderr=subprocess.DEVNULL))
run('surface_walk.py',439,e['x'],e['y'])
run('battle_batch.py',['Mienshao','Arcanine'][a.next==152],0,'--foes','Jellicent,Mamoswine,Slurpuff,Druddigon','--double','--turns',0)
print('NEXT PAIR READY',flush=True)
