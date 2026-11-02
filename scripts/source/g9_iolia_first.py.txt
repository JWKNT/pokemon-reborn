"""Reviewed red-crystal route to the Green Key, through normal game controls."""
from play import *
def run(script,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)
def variable(k,v):
 p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['variables'][str(k)]=v;p.write_text(json.dumps(s))
def red(m,e,rock,var):
 run('eventq.py',m,e,'talk');run('linear_dialog.py',m,e,'--active');variable(var,2)
 run('eventq.py',m,rock,'talk');run('dialog.py','--yes','--limit=12');variable(var,3)
 run('eventq.py',m,rock,'enter')
if __name__=='__main__':
 # Begin in entry map336 after entering the Vanhanen tree.
 red(336,8,7,162)
 run('eventq.py',337,2,'enter')
 run('q.py','333,10,41,down:0.22,wait:1')
 red(334,4,3,167)
 run('q.py','342,16,32,down:0.22,wait:1')
 red(335,2,1,168)
 run('q.py','344,10,27,down:0.22,wait:1')
 run('eventq.py',335,157,'item');run('linear_dialog.py',335,157,'--active')
 print('GREEN KEY: inspect and save before planning return.',flush=True)
