"""Normal-input continuation of the six-pillar Zeraora path after Ein's rescue.

Installed Map847 event pages supply the order. Saves verify each completed
pillar, and existing route/dialogue guards stop on unexpected menus or battles.
"""
from play import *

statefile=ROOT/'notes/navigation-state.json'
def run(script,*args):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],check=True)

for event,before,after in [(7,8,9),(8,9,10),(9,10,11),(10,11,12),(11,12,13)]:
    progress=json.loads(statefile.read_text())['variables']['616']
    if progress>=after:
        continue
    assert progress==before, ('Pillar sequence review',progress,before)
    if event==10:
        run('eventq.py',847,129,'item')  # Inspected Max Repel, short detour.
    run('eventq.py',847,event,'talk')
    run('dialog.py','--limit=60','--story-burst')
    run('checkpoint.py',f'Postgame264-Pillar{event-5}')
    actual=json.loads(statefile.read_text())['variables']['616']
    assert actual==after, ('Pillar completion review',event,actual,after)
    print('PILLAR VERIFIED',event-5,'quest',actual,flush=True)
