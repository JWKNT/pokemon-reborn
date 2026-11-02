"""Execute a reviewed route, escaping approved wild encounters and retrying interrupted steps."""
from play import *
foes={'noibat','woobat','hoobat','klink','klang','mawile','skorupi','drapion','geodude','graveler','trubbish','rattata','pancham','pidove','scraggy','purrloin','voltorb','togedemaru','yamask','duskull','beedril','beedrill','pidgeotto','fearow','bunnelby','foongus','palpitoad','wooper','shellos','gloom','yanma','quagsire','amoonguss','shelmet','zubat','paras','golbat','parasect','ariados','diglett','dugtrio','slugma','magcargo','numel','throh','sawk','arbok','ekans','muk','koffing','weezing','cubone','marowak','munna','venipede','whirlipede','pineco','inkay','sandslash','onix','hippopotas','durant','sandile','krokorok','komala','tauros','bouffalant','miltank','audino','deerling','stantler','karrablast','rapidash','ponyta','cherubi','cherrim','linoone','primeape','venomoth','venonat','ninjask','butterfree','vivillon','heracross','unown','elgyem','baltoy','claydol','hypno','drowzee','natu','xatu','sigilyph','furfrou','kecleon','girafarig','ledyba','ledian','spinarak','mothim','sudowoodo','bewear','passimian','kangaskhan','skiddo','gogoat','mudbray','mudsdale'}
steps=[]
for args in json.load(open(sys.argv[1])):
 if args[0]=='q' and len(args)>2:steps.extend([['q',step] for step in args[1:]])
 else:steps.append(args)
for i,args in enumerate(steps):
 for attempt in range(15):
  print('STEP',i,args,'attempt',attempt+1,flush=True)
  rc=subprocess.call([sys.executable,str(ROOT/'scripts'/(args[0]+'.py')),*map(str,args[1:])])
  if not rc:break
  observed=snap();t=' '.join(x['text'] for x in observed).lower()
  enemy=' '.join(x['text'] for x in observed if x['y']<.37).lower()
  if not any(n in enemy for n in foes) or not ('hp' in t or 'fight' in t):raise SystemExit('Unexpected interruption')
  if subprocess.call([sys.executable,str(ROOT/'scripts/flee.py')]):raise SystemExit('Escape failed')
 else:raise SystemExit('Route retry limit')
