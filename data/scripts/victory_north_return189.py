"""Reviewed next stage of the first Victory Road rail puzzle, normal controls."""
from play import *
def run(name,*args):subprocess.run([sys.executable,str(ROOT/'scripts'/(name+'.py')),*map(str,args)],check=True)
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['switches']['1116'] and s['positions']['786']['40']==[60,51]
run('victory_rail_queue',ROOT/'work/189-north-rail-plan.json','NorthRails189')
run('overworld')
run('victory_boulder_push',786,41,'up',2)
run('checkpoint','Boulder189-north-clear')
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['positions']['786']['41']==[53,25]
run('q','786,44,45,up,c,wait:3')
run('dialog','--limit=5')
run('eventq',786,110,'item')
run('dialog','--limit=6')
run('checkpoint','Tyranitarite189')
s=json.loads((ROOT/'notes/navigation-state.json').read_text());assert s['switches']['1284']
run('q','786,44,43,down,c,wait:3')
run('dialog','--limit=5')
run('victory_rail_queue',ROOT/'work/189-return-rail-plan.json','ReturnRails189')
