from g9_iolia_first import *
run('eventq.py',336,7,'talk');run('dialog.py','--yes','--limit=12');variable(162,3)
run('eventq.py',336,7,'enter');run('eventq.py',337,2,'enter')
run('q.py','333,10,41,down:0.22,wait:1')
red(334,4,3,167);run('q.py','342,16,32,down:0.22,wait:1')
red(335,2,1,168);run('q.py','344,10,27,down:0.22,wait:1')
run('eventq.py',335,157,'item');run('linear_dialog.py',335,157,'--active')
print('GREEN KEY: inspect and save.',flush=True)
