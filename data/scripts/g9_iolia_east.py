from g9_iolia_middle import *
# Continue after middle green crystal 136.
run('q.py','335,35,0,up:0.22,wait:1')
run('q.py','334,31,0,up:0.22,wait:1')
run('eventq.py',333,73,'smash')
red(333,16,17,165)
run('q.py','341,12,27,down:0.22,wait:1')
run('q.py','334,41,22,down:0.22,wait:1')
crystal(335,141,448)
# Return via the same eastern cave. The crystal opens rocks on the far bank.
run('q.py','335,41,0,up:0.22,wait:1')
run('q.py','334,39,2,up:0.22,wait:1')
run('q.py','341,9,8,left:0.22,wait:1')
print('EAST CRYSTAL OPEN: inspect respawned green rocks before return.',flush=True)
