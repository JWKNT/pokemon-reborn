"""Reviewed first Glitch team only; bounded normal UI and public HUD guards."""
import os,subprocess,sys
os.environ['REBORN_FAST_KEYS']='1'
def run(*args):subprocess.run([sys.executable,'scripts/'+args[0]+'.py',*args[1:]],check=True)
run('battle_batch','Mewtwo','3','--foes','Roserade','--turns','3','--watch','--min-hp','.40','--status-move')
print('STOP: review three public Amnesia turns and HP before attacking.',flush=True)
