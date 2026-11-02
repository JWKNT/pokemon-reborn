"""Bounded normal-UI Jirachi memory route. Save after each completed scene to verify its story gate."""
import subprocess,sys,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1')
def run(script,*args):
 subprocess.run([sys.executable,str(R/'scripts'/script),*map(str,args)],check=True)
def scene(e,page,stage,kind='talk',follow=None):
 run('eventq.py',854,e,kind)
 args=[854,e,'--source-page',page,'--burst','--log-scripted-bgm']
 if follow: args += ['--follow-source',854,follow[0],'--follow-source-page',follow[1]]
 run('linear_dialog.py',*args)
 run('checkpoint.py')
 state=json.loads((R/'notes/navigation-state.json').read_text())
 assert state['variables']['615']==stage,(e,stage,state['variables']['615'])
 print('MEMORY STAGE VERIFIED',stage,flush=True)
def touch(e,page,stage,follow=None):
 data=json.loads(subprocess.check_output(['ruby',str(R/'scripts/event_dump.rb'),'854',str(e)],stderr=subprocess.DEVNULL))
 rc=subprocess.call([sys.executable,str(R/'scripts/q.py'),f"854,{data['x']},{data['y']}"])
 if rc not in (0,2):raise SystemExit(rc)
 args=[854,e,'--source-page',page,'--burst','--log-scripted-bgm']
 if follow:args+=['--follow-source',854,follow[0],'--follow-source-page',follow[1]]
 run('linear_dialog.py',*args)
 run('checkpoint.py')
 actual=json.loads((R/'notes/navigation-state.json').read_text())['variables']['615']
 assert actual==stage,(e,stage,actual)
 print('MEMORY STAGE VERIFIED',stage,flush=True)
if __name__=='__main__':
 scene(3,1,3)
 scene(6,1,4)
 scene(11,0,6)
 scene(12,0,7)
