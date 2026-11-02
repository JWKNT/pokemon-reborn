"""Walk the inspected future hall's eight story triggers using normal input."""
from play import *
from locate import locate

events = [8, 11, 12, 13, 14, 15, 16, 17]
start = int(sys.argv[1]) if len(sys.argv) > 1 else 8
assert start in events
for eid in events[events.index(start):]:
    source = json.loads(subprocess.check_output(['ruby', str(ROOT/'scripts/event_dump.rb'), '845', str(eid)], stderr=subprocess.DEVNULL))
    page = source['pages'][1]
    commands = page['list']
    assert page['trigger'] == 1 and source['x'] == 17
    assert not any(c['code'] in [102,103,104,301] or 'pbTrainerBattle' in str(c['parameters']) for c in commands)
    updates = [c['parameters'][4] for c in commands if c['code']==122 and c['parameters'][:4]==[618,618,0,0]]
    assert len(updates)==1
    if not (eid == start and '--active-dialogue' in sys.argv):
        mid,x,y = locate(845)
        assert mid == 845
        plan = ROOT/'work/celebi-future-step.json'
        plan.write_text(json.dumps([[845,x,y,17,source['y'],[]]]))
        routed = subprocess.run([sys.executable,str(ROOT/'scripts/queue_route.py'),str(plan),'--from-verified'])
        assert routed.returncode in [0,2], 'Route failed outside a story interruption'
    text = read()
    print(text,flush=True)
    assert len(re.sub('[^a-z]','',text.lower().replace('pokemon reborn',''))) > 10, 'Expected story trigger'
    import difflib
    norm = lambda z: re.sub('[^a-z]','',z.lower().replace('pokemon reborn',''))
    first = next(c['parameters'][0] for c in commands if c['code']==101)
    assert difflib.SequenceMatcher(None,norm(text),norm(first)).ratio() > .6, 'Unexpected dialogue at story trigger'
    run = subprocess.run([sys.executable,str(ROOT/'scripts/linear_dialog.py'),'845',str(eid),'--source-page','1','--burst','--log-scripted-bgm'],capture_output=True,text=True)
    print(run.stdout,flush=True)
    assert run.returncode == 0 and 'OVERWORLD' in run.stdout, run.stderr
    # Planning notes only: source-assigned progress after observed complete scene.
    path = ROOT/'notes/navigation-state.json'
    state = json.loads(path.read_text())
    state['variables']['618'] = updates[0]
    state.setdefault('observed_progress',[]).append({'epoch':time.time(),'variable':618,'value':updates[0],'evidence':f'Observed completed future hall845 event{eid}, installed page1 final assignment; navigation only.'})
    path.write_text(json.dumps(state))
    print('FUTURE STORY COMPLETE',eid,updates[0],flush=True)
