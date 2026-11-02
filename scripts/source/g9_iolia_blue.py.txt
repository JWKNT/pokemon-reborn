"""Reviewed return from the Green Key and route to the Blue Key."""
from g9_iolia_first import *
run('q.py','335,23,44,up:0.22,wait:1','344,16,8,left:0.22,wait:1','335,13,4,up:0.22,wait:1','342,17,9,right:0.22,wait:1','334,10,0,up:0.22,wait:1')
run('eventq.py',333,62,'talk');run('linear_dialog.py',333,62,'--active')
p=ROOT/'notes/navigation-state.json';s=json.loads(p.read_text());s['switches']['443']=True;p.write_text(json.dumps(s))
run('eventq.py',333,65,'smash')
run('q.py','333,16,41,down:0.22,wait:1')
red(334,2,1,166)
run('linear_dialog.py',334,1,'--active','--burst')
run('q.py','342,21,32,down:0.22,wait:1')
run('eventq.py',335,158,'item');run('linear_dialog.py',335,158,'--active')
print('BLUE KEY: inspect and save.',flush=True)
