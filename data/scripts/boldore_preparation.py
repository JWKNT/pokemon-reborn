"""Bounded normal-control preparation for the owned Sturdy Boldore.

No runtime reads or save mutation. Each phase starts at its named checkpoint;
normal controls, capture guards, and public menu/battle guards remain active.
"""
import json, os, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(name,*args):
    print('STAGE',name,*args,flush=True)
    env=dict(os.environ,REBORN_COORD_CACHE='1')
    env.pop('REBORN_FAST_KEYS',None)
    if name in ('eventq','q','connected_walk'):env['REBORN_FAST_KEYS']='1'
    subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True,cwd=R,env=env)
def checkpoint(label):
    run('checkpoint',label)
    return json.loads((R/'notes'/f'{label}-status.json').read_text())
phase=sys.argv[1]
if phase=='candies':
    first,last=map(int,sys.argv[2:4]);assert 3<=first<=last<=6
    for n in range(first,last+1):
        run('saphira_indra_candy','--turbo')
        run('eventq',355,118,'talk');run('heal')
        st=checkpoint(f'Saphira176-Indra{n}')
        assert all(m['hp']==m['totalhp'] for m in st['party'])
        assert st['bag']['contents']['EXPCANDYXL']>=5*n
elif phase=='linkstone':
    run('fly_to',525,'--carrier','Tranquill')
    run('connected_walk',525,551,15,12)
    run('field_repel','Super Repel')
    run('eventq',551,15,'enter');run('eventq',184,2,'enter')
    run('eventq',185,6,'item')
    st=checkpoint('Saphira176-LinkStone')
    assert st['bag']['contents']['LINKSTONE']>=1
elif phase=='evolve':
    run('field_medicine','Link Stone','Boldore','--pocket','items')
    run('candy_progress');run('overworld')
    st=checkpoint('Saphira176-Gigalith')
    mon=next(m for m in st['party'] if m['species']=='GIGALITH')
    assert mon['ability']=='STURDY'
elif phase=='level':
    run('train_candy_one','Gigalith',26,'XL')
    st=checkpoint('Saphira176-Gigalith95')
    mon=next(m for m in st['party'] if m['species']=='GIGALITH')
    assert mon['level']==95
elif phase in ('ev-travel','ev-from-circus'):
    if phase=='ev-travel':
        run('eventq',185,1,'enter');run('eventq',184,1,'enter')
        run('connected_walk',551,525,21,23)
    run('fly_to',519,'--carrier','Tranquill')
    run('give_held','Power Weight','Gigalith')
    run('party_front','Gigalith')
    run('q','519,9,60,left,wait:2','530,94,13,right,wait:2','519,29,11,right,wait:2','513,15,8,right,wait:2','519,58,11,right,wait:2','633,10,8')
    st=checkpoint('Saphira-Gigalith-EV-ready')
    mon=next(m for m in st['party'] if m['species']=='GIGALITH')
    assert mon['ev']==[0,0,0,0,0,0],mon['ev']
elif phase in ('hp-pilot','hp-rest','attack'):
    if phase=='attack':run('give_held','Power Bracer','Gigalith')
    count={'hp-pilot':1,'hp-rest':7,'attack':8}[phase]
    run('train_wild_bulk','Arcanine',1,count,'--targets','Noibat,Woobat',
        '--flex-targets','--ev-ledger','--hunter','Gigalith','--relead-hunter',
        '--expire-repel','--dense-horizontal','--recover-slot',3,'--recover-below',.6)
    st=checkpoint('Saphira-Gigalith-'+phase)
    mon=next(m for m in st['party'] if m['species']=='GIGALITH')
    expected={'hp-pilot':[32,0,0,0,0,0],'hp-rest':[252,0,0,0,0,0],
              'attack':[252,252,0,0,0,0]}[phase]
    assert mon['ev']==expected,(mon['ev'],expected)
else:
    raise SystemExit('Unknown phase')
