"""Repeat only the proven Sunday Fawkes matchup, stopping when saved stock suffices."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
first=int(sys.argv[1]);assert 2<=first<=6
prior=f'Postgame289-Fawkes{first-1}'
for number in range(first,7):
 p=R/'work'/f'{prior}-candy-plan.json'
 result=subprocess.run([sys.executable,str(R/'scripts/postgame_candy_spend.py'),prior,'125','--plan-only'],capture_output=True,text=True)
 assert p.exists(),result.stdout+result.stderr
 plan=json.loads(p.read_text());print('CANDY CHECK',prior,'need',plan['need'],'stock',plan['stock'],flush=True)
 if plan['need']<=plan['stock']:
  assert result.returncode==0
  print('ENOUGH CANDY',prior,flush=True);break
 assert result.returncode==1 and 'Earn more candy before spending' in result.stderr,result.stderr
 prior=f'Postgame289-Fawkes{number}'
 subprocess.run([sys.executable,str(R/'scripts/fawkes288_round.py'),prior],check=True)
else:
 result=subprocess.run([sys.executable,str(R/'scripts/postgame_candy_spend.py'),prior,'125','--plan-only'],check=True)
 print('ENOUGH CANDY',prior,flush=True)
