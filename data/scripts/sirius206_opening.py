"""Bounded, visible-screen Sirius retry opening; stops after two turns."""
from play import *
def expect(name):
 t=re.sub('[^a-z]','',read().lower())
 assert 'whatwill'+name.lower()+'do' in t, ('Unexpected actor; no action selected',t)
 assert 'manectric' in t and 'marowak' in t, ('Lead pair changed; review',t)
def run(name,*args):
 subprocess.run([sys.executable,str(ROOT/'scripts'/f'{name}.py'),*args],check=True)
expect('Arcanine');run('battle_move','1','3','--watch')
expect('Swampert');run('battle_item','X Attack','Swampert')
expect('Arcanine');run('battle_move','2','1','--watch')
expect('Swampert');run('battle_item','X Speed','Swampert')
print('TWO TURN OPENING COMPLETE; inspect replacements and HP',flush=True)
