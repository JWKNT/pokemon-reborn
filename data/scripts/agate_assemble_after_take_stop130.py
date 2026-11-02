"""Resume ONLY after verified first normal PC exchange; never repeat it."""
import argparse,json,hashlib
from pathlib import Path
from agate_party_assemble import Runner,preflight,ROOT
from play import read
before=ROOT/'notes/Agate-Ricardo-won130-status.json';navpath=ROOT/'notes/Agate-Ricardo-won130-navigation.json'
status=json.loads(before.read_text());nav=json.loads(navpath.read_text())
oldpath=ROOT/'work/agate-party-assemble-130-after-swap1.json';old=json.loads(oldpath.read_text())
assert old['status']=='stopped-for-actual-state-review' and old['pending']=={'script':'take_held','args':['Kricketune','Focus Sash','--menu-open'],'epoch':old['pending']['epoch']}
args=argparse.Namespace(journal=ROOT/'work/agate-party-assemble-130-after-take-stop.json',status=before,navigation=navpath,phase='agate-assemble',checkpoint='Agate-final-six-south-ready130')
proposal=preflight(status,nav,phase='agate-assemble');runner=Runner(args,status,nav,proposal)
runner.journal['resume_review']={'prior':str(oldpath.relative_to(ROOT)),'sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'completed_first_exchange_not_replayed':True};runner.write()
try:
 text=read().lower();assert 'do what with kricketune' in text and 'summary' in text and 'rock smash' in text, 'Actual fresh Kricketune Summary required'
 runner.expected[1]='Kricketune';out=runner.run('take_held','Kricketune','Focus Sash','--menu-open');runner.settle();runner.record('visible-held-item-taken',owner='Kricketune',item='Focus Sash')
 runner.exchange(6,'Hexan','Kricketune')
 runner.open_pause_choice('Bag');runner.run('give_held','Focus Sash','Hexan','--bag-open');runner.settle();runner.arrange()
 runner.active_source(752,4,0);runner.run('eventq',752,4,'talk')
 welcome=read().lower();assert 'welcome' in welcome or 'rest' in welcome
 runner.run('choose_dialog','Yes|No','Yes');runner.run('heal');runner.position(752)
 runner.active_source(752,8,0);runner.run('eventq',752,8,'enter');runner.position(763,(763,46,70))
 runner.party_check();runner.stage(52);runner.position(763,(763,46,70));runner.checkpoint_proof(proposal)
 print('AGATE FINAL SIX ASSEMBLED; FIRSTSWAPNOTREPLAYED',flush=True)
except BaseException as error:
 runner.journal.update(status='stopped-for-actual-state-review',verified=False);runner.record('stop',reason=str(error),error=type(error).__name__);raise
