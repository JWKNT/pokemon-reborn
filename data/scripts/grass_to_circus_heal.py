"""Reviewed Route 2 elevator itinerary, followed by circus nurse."""
from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/(s+'.py')),*map(str,a)],check=True)
run('use_field_item','Super Repel')
run('q','358,54,61,right:.12,wait:2','365,10,61,up:.12,wait:2','365,8,48,up:.03,c,wait:1')
run('choose_dialog','Agate Circus|Route 2','Agate Circus')
act('c:.12','wait:1')
p=ROOT/'notes/navigation-state.json';j=json.loads(p.read_text());j['variables']['74']=0;p.write_text(json.dumps(j))
run('q','365,9,51,down:.12,wait:2','365,15,35,right:.12,wait:2')
run('eventq',355,118,'talk');run('heal');run('checkpoint','Circus-Blake-ready')
