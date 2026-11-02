"""Give this travel party Rock Smash through normal TM use and retry the obstacles."""
import subprocess,sys,json
from pathlib import Path
def run(s,*a):subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
run('overworld');run('teach_machine','TM94','Giratina','Rock Smash',2)
p=Path('notes/navigation-overrides.json');j=json.loads(p.read_text());j['552']=[x for x in j.get('552',[])if int(x)not in[29,30]];p.write_text(json.dumps(j,indent=2)+'\n')
p=Path('work/389-meteor-cave-queue.json');j=json.loads(p.read_text());j.update(done=0,pending=None);p.write_text(json.dumps(j,indent=2)+'\n')
run('meteor389_cave_resume')
