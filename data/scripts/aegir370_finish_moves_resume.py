from play import *
def run(s,*a):
 print('AEGIR MOVES',s,*a,flush=True)
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('teach_machine','TM80','Rayquaza','Rock Slide',1)
run('give_held','Wide Lens','Rayquaza')
run('city_enter',116,521)
run('fly_to',519,'--carrier','Zapdos')
run('city_enter',519,38)
run('eventq',38,3,'talk');run('heal')
run('checkpoint','Aegir369-ReminderComplete')
