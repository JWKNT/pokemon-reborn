"""Run a reviewed sequence of existing UI helpers, aborting on any interruption.
JSON entries: [script basename, argument, ...]. No game-state mutations outside UI.
"""
import json,subprocess,sys,pathlib,time
r=pathlib.Path(__file__).resolve().parent
source=pathlib.Path(sys.argv[1]).resolve()
steps=json.loads(source.read_text())
journal=r.parent/'work/active-steps-progress.json'
def record(index,args,state,**extra):
 journal.write_text(json.dumps(dict(plan=str(source),index=index,args=args,
                                   state=state,total=len(steps),epoch=time.time(),
                                   **extra),indent=2)+'\n')
for i,args in enumerate(steps):
 print('STEP',i,args,flush=True)
 record(i,args,'running')
 try:
  subprocess.run([sys.executable,str(r/(args[0]+'.py')),*map(str,args[1:])],check=True)
 except subprocess.CalledProcessError as error:
  record(i,args,'interrupted',returncode=error.returncode)
  raise
 record(i,args,'completed',next_index=i+1)
