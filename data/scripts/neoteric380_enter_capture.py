"""Enter only the source-reviewed, separate legendary capture after a saved victory."""
from play import *
species=sys.argv[1];assert species in ['Mewtwo','Mew']
event=130 if species=='Mewtwo'else 126
(ROOT/'notes/battle-control.json').write_text(json.dumps(dict(stop=False,expected_foes=[species]),indent=2)+'\n')
p=ROOT/f'work/380-{species.lower()}-capture.json';assert not p.exists(),'Encounter already registered; review before retry'
p.write_text(json.dumps(dict(species=species,session=380,start_epoch=time.time(),event=event),indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'895',str(event),'talk'],check=True)
t=read();assert species.lower() in t.lower().replace('meutwo','mewtwo').replace('meш','mew'),t
act('c','wait:3')
subprocess.run([sys.executable,str(ROOT/'scripts/battle_ready.py')],check=True)
