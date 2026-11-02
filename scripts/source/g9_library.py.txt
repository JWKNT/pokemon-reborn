from play import *
import nav
def run(*a):subprocess.run([sys.executable,str(ROOT/'scripts'/a[0]),*a[1:]],check=True)
for e in [9,8,7,6,5,4]:
 run('eventq.py','332',str(e),'talk');run('choose_dialog.py','Yes|No','Yes');run('linear_dialog.py','332',str(e),'--active','--past-choice','--burst')
run('eventq.py','332','10','item');run('give_held.py','Spell Tag','Cofagrigus')
run('eventq.py','332','13','item')
nav.save();print(read(),flush=True)
