from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('linear_dialog',827,35,'--source-page',10,'--until-choice');run('choose_dialog','Yes|No','Yes');run('linear_dialog',827,35,'--source-page',10,'--past-choice','--after-last-choice');run('checkpoint','Idyll317-Quest')
run('city_enter',827,826);run('city_enter',826,527);run('fly_to',530,'--carrier','Zapdos')
run('party_front','Mawile');run('field_repel','Max Repel');run('eventq',530,8,'enter')
q=ROOT/'work/317-eve-approach.json';q.write_text(json.dumps([[878,0,0,82,86,[]]]));run('queue_route',q)
run('checkpoint','Idyll317-EvePrepared')
