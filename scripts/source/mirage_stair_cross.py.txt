"""Cross one installed automatic Mirage staircase through normal controls."""
from play import *
from locate import locate
mid=674;eid=154
v=json.loads(subprocess.check_output(['ruby',str(ROOT/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL));e=v['events'][str(eid)]
cs=e['list'];moves=[m['code']for c in cs if c['code']==209 and c['parameters'][0]==-1 for m in c['parameters'][1]['list']]
assert (e['x'],e['y'],e['trigger'])==(14,32,1) and moves.count(4)==8 and 37 in moves and 38 in moves
assert not any(c['code']in[102,103,104,301,201]for c in cs)
assert locate(mid)==(mid,14,33)
act('up:.12','wait:3');actual=locate(mid);assert actual in [(674,14,24),(674,14,25)],actual
p=ROOT/'notes/navigation-state.json';n=json.loads(p.read_text());edge=[14,33,'up',actual[1],actual[2]]
if edge not in n.setdefault('edges',{}).setdefault(str(mid),[]):n['edges'][str(mid)].append(edge)
n['observed_mirage_stair154']={'epoch':time.time(),'arrival':actual,'source':'Installed8-Up automatic route, actual public coordinate popup verified'};p.write_text(json.dumps(n,indent=2)+'\n')
print('MIRAGE STAIR CROSS VERIFIED',actual,flush=True)
