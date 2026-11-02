"""Model an OBSERVED water-control interaction into navigation notes only.

Interprets the installed, deterministic control/common-event commands. It never
edits game files or runs commands inside the game. Invoke after the real button
has been pressed, while notes still describe the state before that press.
"""
from play import *
from locate import locate
import copy

from wtc_model import predict
old,eid,new=map(int,sys.argv[1:4])
p=ROOT/'notes/navigation-state.json';state=json.loads(p.read_text())
state,current,budget=predict(state,old,eid)
positions=state['positions'];vars=state['variables']
def value(i):return vars.get(str(i),0) or 0
assert current==new,('Control-model map mismatch',current,new)
assert locate(new)[0]==new,'Observed transfer required before committing notes'
evidence={'epoch':time.time(),'from_map':old,'event':eid,'to_map':new,'instructions':budget,'positions':positions[str(new)],'water_levels':{str(k):value(k)for k in range(256,265)}}
(ROOT/'work'/f'wtc-control-{int(time.time())}.json').write_text(json.dumps(evidence,indent=2))
p.write_text(json.dumps(state))
print('OBSERVED WATER CONTROL MODELED IN NOTES',old,eid,new,budget,flush=True)
