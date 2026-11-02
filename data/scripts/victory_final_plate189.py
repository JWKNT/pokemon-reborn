"""Finish the reviewed B1F pressure plate and exit cart, then pause in party."""
from play import *
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['variables']['487']==0 and s['positions']['786']['41']==[53,25]
run('overworld')
run('victory_boulder_queue',ROOT/'work/189-boulder41-final-plan.json',41,'FinalPlate189')
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['switches']['1117']
run('victory_rail_queue',ROOT/'work/189-exit-cart-plan.json','ExitCart189')
