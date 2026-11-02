"""Use the existing pure surface planner without importing input-owning nav."""
from route_readonly import ROOT,route
import ast,copy,heapq,re
WATER={5,6,7,9}
tree=ast.parse((ROOT/'scripts/surface_plan.py').read_text())
functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['tag','surface_plan']]
assert len(functions)==2
exec(compile(ast.Module(body=functions,type_ignores=[]),'surface-readonly-extract','exec'))
