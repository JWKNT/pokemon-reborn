from play import *
def run(s,*a):subprocess.run([sys.executable,str(ROOT/'scripts'/f'{s}.py'),*a],check=True)
run('battle_item','X Defend','Mewtwo');act('wait:1');run('battle_ready');run('battle_move','2','--watch');run('battle_ready')
