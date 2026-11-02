"""Follow the installed two-rock Railcave route using ordinary recorded input.

Map251 event5 supplies the deterministic negative-progress sequence. Only
navigation notes are updated after an observed transfer; game data is untouched.
Start in the Railcave. Each ordinary save verifies actual puzzle progress,
because identical room coordinates alone cannot prove exactly one transition.
"""
from play import *
from locate import locate

statefile=ROOT/'notes/navigation-state.json'
directions=[4,4,1,4,1,2,1,4,3,4]
events={1:3,2:2,3:4,4:1}
for attempt in range(20):
    actual=locate()
    if actual[0]==252:
        break
    assert actual[0]==251, ('Railcave room review',actual)
    subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py')],check=True)
    state=json.loads(statefile.read_text())
    progress=state['variables']['146']
    assert -9<=progress<=0, ('Puzzle progress review',progress)
    direction=directions[-progress]
    assert state['variables']['148']==direction
    print('SAVED TWO-ROCK PROGRESS',progress,'NEXT',direction,flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/eventq.py'),'251',str(events[direction]),'enter'],check=True)
else:
    raise SystemExit('Railcave bounded doorway limit')
subprocess.run([sys.executable,str(ROOT/'scripts/checkpoint.py'),'Postgame264-RailcaveReached'],check=True)
