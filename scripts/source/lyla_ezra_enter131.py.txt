"""Ordinary paired encounter from source-reviewed staging; one trigger only."""
import subprocess,sys,json
from play import ROOT,act
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*map(str,a)],check=True)
run('trainer_music','start','NWCultistF','Lyla & Ezra','--battle-track','Atmosphere- Majesty')
p=ROOT/'work/active-trainer-music.json';d=json.loads(p.read_text());d['victory']='Atmosphere- Majesty';d['event_music_evidence']='Map763 E45/46 command132 Majesty and133 empty AudioFile; installed Audio no-op empty name';p.write_text(json.dumps(d,indent=2))
act('right:0.12','wait:.5')
run('trainer_enter',763,45,'NWCultistF','Lyla & Ezra','--paired-event',46,'--active-dialogue','--resume-intro')
