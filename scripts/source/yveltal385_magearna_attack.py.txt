from play import *
for script,args in [('battle_item',['Ultra Potion','Magearna']),('battle_move',['3','--watch']),('battle_move',['0','--watch'])]:
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{script}.py'),*args],check=True)
