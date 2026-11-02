"""Complete the source-reviewed post-Eclipse scene, then save at the Nightclub."""
import subprocess,sys

def run(s,*a):subprocess.run([sys.executable,'scripts/'+s+'.py',*map(str,a)],check=True)
run('victory_outro')
run('major_attempt','victory','work/major-223.json',386)
run('trainer_music','finish')
run('linear_dialog',889,40,'--source-page',0,'--after-last-battle','--past-battle','--until-choice','--burst')
run('choose_dialog','Yes|No','Yes')
run('linear_dialog',889,40,'--source-page',0,'--after-last-choice','--past-choice','--past-battle','--burst')
run('checkpoint','Picnic386-EclipseWon')
