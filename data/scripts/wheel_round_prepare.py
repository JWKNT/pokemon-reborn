"""Register and select an inspected Battle Wheel round; stop at first battle command."""
import argparse,json,os,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('round',type=int,choices=[2,3,4,5]);p.add_argument('names',nargs=3);p.add_argument('--session',type=int,default=269);a=p.parse_args()
os.environ.update(REBORN_FAST_KEYS='1',REBORN_COORD_CACHE='1',REBORN_ROUTE_CHUNK='84')
def run(n,*args):
 print('WHEEL STAGE',n,*args,flush=True)
 subprocess.run([sys.executable,str(R/'scripts'/f'{n}.py'),*map(str,args)],check=True)
# These are static installed source pages, not runtime enemy inspection.
source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/event_dump.rb'),'867','25'],stderr=subprocess.DEVNULL))
page=2*a.round-2;cs=source['pages'][page]['list']
assert not any(c['code'] in [102,103,104] or 'pbTrainerBattle' in str(c['parameters']) for c in cs)
run('checkpoint',f'Meloetta{a.session}-BeforeRound{a.round}Announcement')
run('eventq',867,25,'talk');run('linear_dialog',867,25,'--source-page',page,'--burst','--log-scripted-bgm')
label=f'Meloetta{a.session}-Round{a.round}'
run('checkpoint',label)
s=json.loads((R/'notes'/f'{label}-navigation.json').read_text());assert s['variables']['627']==2*a.round+2
party=json.loads((R/'notes'/f'{label}-status.json').read_text())['party']
assert all(any(m['name']==n and m['hp']==m['totalhp'] for m in party) for n in a.names)
rosters={2:('JULIA','Julia',['Galvantula','Rotom','Sploosh','Ampharos']),3:('BRELOOM','CL:4R1-C3',['Magnezone','Magearna','Breloom','CL:4R1-C3']),4:('RINGMASTER','Alistasia',['Hawlucha','Blaziken','Primarina']),5:('CASS','Cass',['Naganadel','Necrozma','Rayquaza'])}
cls,name,foes=rosters[a.round]
if a.round==5:
 if s['switches'].get('976',False):foes=['Ninetales','Amethyst','Cinccino','Meech','Gardevoir']
(R/'notes/battle-control.json').write_text(json.dumps({'stop':False,'expected_foes':foes},indent=2)+'\n')
run('eventq',867,63,'talk');run('play','c','wait:.5','c','wait:.8')
run('wheel_select_three',*a.names)
run('linear_dialog',867,63,'--source-page',2*a.round,'--command-range',11,14,'--burst')
run('play','c','wait:3')
opts=['--source-page',a.round-1,'--active-dialogue','--burst-dialogue']
if a.round==5 and s['switches'].get('976',False):opts[1]=5
if a.round==4:
 run('choose_dialog','Yes|No','No')
 opts+=['--past-choice']
run('trainer_enter',868,3,cls,name,*opts)
