"""Record an observed completed event in navigation notes only; never edit game data."""
import json,pathlib,sys
m,e=map(int,sys.argv[1:3]);ch=sys.argv[3] if len(sys.argv)>3 else 'A'
assert ch in 'ABCD' and len(ch)==1
p=pathlib.Path(__file__).resolve().parents[1]/'notes/navigation-state.json'
s=json.loads(p.read_text());s.setdefault('self_switches',{})[f'{m},{e},{ch}']=True
p.write_text(json.dumps(s));print('Navigation event marked',m,e,ch)
