"""Update a navigation note only after observing the triggering coordinate."""
from play import *
from locate import locate
mid,x,y,number,value=map(int,sys.argv[1:6]);assert value in [0,1]
actual=locate(mid);assert actual==(mid,x,y),(actual,(mid,x,y))
p=ROOT/'notes/navigation-state.json';v=json.loads(p.read_text());v.setdefault('switches',{})[str(number)]=bool(value);p.write_text(json.dumps(v));print('OBSERVED ROUTE SWITCH',number,value,'at',actual,flush=True)
