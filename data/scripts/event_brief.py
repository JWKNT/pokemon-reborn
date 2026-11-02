import subprocess,json,sys
v=json.loads(subprocess.check_output(['ruby','scripts/event_dump.rb',*sys.argv[1:]],stderr=subprocess.DEVNULL))
for i,p in enumerate(v['pages']):
 print('PAGE',i,'at',v['x'],v['y'],'COND',p['condition'])
 for c in p['list']:
  if c['code'] in [101,401,102,111,121,122,123,201,355,655]:print(c['code'],c['parameters'])
