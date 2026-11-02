"""Three reviewed Arcanine/Klinklang cycles, public command/HP guards each turn."""
from play import *
cycles=int(sys.argv[1]) if len(sys.argv)>1 else 3
assert 1<=cycles<=5
partner=sys.argv[sys.argv.index("--partner")+1] if "--partner" in sys.argv else "Klinklang"
assert partner in ["Klinklang","Excadrill"]
turbo='--turbo' in sys.argv
control=ROOT/'notes/current-run-control.json'
def turbo_state(enabled):
 d=json.loads(control.read_text());d.update(battle_turbo_enabled=enabled,battle_turbo=enabled,overworld_turbo_enabled=False);control.write_text(json.dumps(d,indent=2))
if turbo:
 d=json.loads(control.read_text());assert not d.get('battle_turbo_enabled',False),'Turbo starting state must be verified OFF'
 assert 'fight' in read().lower(),'Turbo only in observed battle command screen'
 act('m:.12');turbo_state(True)
try:
 for index,name in enumerate([partner,'Arcanine']*cycles,1):
  t=read();assert 'fight' in t.lower() and any(n in t.lower() for n in ['aerodactyl','herodactyl']),t
  result=subprocess.run([sys.executable,str(ROOT/'scripts/battle_switch.py'),name],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  print(result.stdout,flush=True);assert result.returncode==0
  t=read();low=t.lower();assert 'fight' in low and name.lower() in low,t
  hp=re.findall(r'(\d+)\s*/\s*(290|362|399)',t);assert hp,'Own HP needs review: '+t
  current,total=map(int,hp[-1]);assert current>=100,(name,current,'Cycle stopped for recovery')
  print('CYCLE VERIFIED',index,name,current,total,flush=True)
finally:
 if turbo:
  act('m:.12');turbo_state(False)
  print('TURBO RESTORED OFF',flush=True)
