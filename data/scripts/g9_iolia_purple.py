from g9_iolia_middle import *
def reset_rocks(m,*ids):
 p=ROOT/'notes/navigation-overrides.json';v=json.loads(p.read_text());v[str(m)]=[e for e in v.get(str(m),[]) if e not in ids];p.write_text(json.dumps(v))
if __name__=='__main__':
 reset_rocks(333,73);reset_rocks(334,7)
 run('eventq.py',333,73,'smash')
 run('q.py','333,31,41,down:0.22,wait:1')
 run('eventq.py',334,7,'smash')
 run('q.py','334,35,22,down:0.22,wait:1')
 run('eventq.py',335,140,'smash');run('eventq.py',335,142,'smash')
 red(335,4,3,169)
 run('q.py','343,24,9,right:0.14,wait:1')
 run('choose_dialog.py','Yes|No','No')
 run('linear_dialog.py',343,6,'--active','--past-choice','--burst');variable(159,20)
 run('eventq.py',343,3,'item');run('linear_dialog.py',343,3,'--active')
 print('PURPLE KEY COLLECTED',flush=True)
