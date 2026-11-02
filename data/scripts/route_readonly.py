"""Expose the existing pure route planner without importing the input-owning nav module."""
import ast,json,heapq,re
from pathlib import Path
from collections import deque
from itertools import groupby
ROOT=Path(__file__).resolve().parents[1]
source=ast.parse((ROOT/'scripts/nav.py').read_text())
functions=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in ['route','action_jump']]
assert len(functions)==2
exec(compile(ast.Module(body=functions,type_ignores=[]),'nav-readonly-extract','exec'))
