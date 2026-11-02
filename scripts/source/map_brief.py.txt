import json,sys
from nav import loadmap
v=loadmap();print('Map',v['map'],'position',v['position'])
for k,e in v['events'].items():
 cmds=e['list'] or []
 lines=[str(c['parameters']) for c in cmds if c['code'] in [101,201,355,655]]
 if e['character'] or any(c['code']==201 for c in cmds):
  print(k,(e['x'],e['y']),e['name'],e['character'],' | '.join(lines)[:1100])
