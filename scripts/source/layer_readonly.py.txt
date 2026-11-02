"""Expose the pure layered planner without importing the UI input owner."""
import ast,copy,json,subprocess,heapq
from route_readonly import ROOT,route,action_jump
DIR={'up':(0,-1,8),'down':(0,1,2),'left':(-1,0,4),'right':(1,0,6)}
CACHE={}
tree=ast.parse((ROOT/'scripts/layer_route.py').read_text())
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['effect','plan']]
assert len(functions)==2
exec(compile(ast.Module(body=functions,type_ignores=[]),'layer-readonly-extract','exec'))
