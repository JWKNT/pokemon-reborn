"""Normal reviewed Seventh Street elevator exit; no save mutation."""
import subprocess,sys,os,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(name,*a):
 env=dict(os.environ,REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
 subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,a)],env=env,check=True)
run('eventq',324,1,'enter');run('eventq',168,12,'enter');run('eventq',168,18,'talk')
from play import act,read
s=read().lower();assert '7th street' in s and 'lapis ward' in s,s
act('down','c','wait:2');s=read();print(s,flush=True);assert 'Lapis Ward Level' in s,s
act('c','wait:1')
f=R/'notes/navigation-state.json';v=json.loads(f.read_text());v['variables']['79']=0;v.setdefault('evidence',[]).append({'kind':'elevator floor','observed':'Lapis Ward Level','variable':79,'value':0});f.write_text(json.dumps(v))
run('eventq',168,11,'enter');run('eventq',168,2,'enter')
