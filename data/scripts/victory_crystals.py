"""Enter Victory Road puzzle 1's clue-derived solution using ordinary controls.
Only a fresh legitimate puzzle checkpoint is accepted. Each bounded push group
is checked via public coordinates; every column is saved normally and the owned
frozen event positions are checked. No hidden answer or game writes are used.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('journal');p.add_argument('--start-column',type=int,default=0,choices=range(3));a=p.parse_args()
 n=R/'notes'/f'{a.label}-navigation.json'; s=R/'notes'/f'{a.label}-status.json';j=R/a.journal
 assert not j.exists() and time.time()-n.stat().st_mtime<120
 assert json.loads(s.read_text())['map']==785
 sol=json.loads((R/'work/186-gem-puzzle1-solution.json').read_text())['solutions'];assert len(sol)==1
 cols=[sol[0][k]for k in ['size','hardness','purity']]
 from play import act,read
 from locate import locate
 history=[]
 def log(**kw):history.append(dict(epoch=time.time(),**kw));j.write_text(json.dumps(history,indent=2)+'\n')
 def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True)
 for col in range(a.start_column,3):
  nav=json.loads(n.read_text());origin=16+6*col
  for row in range(4):
   xx,yy=nav['positions']['785'][str(9+row*3+col)]
   assert yy==11+row and origin<=xx<=origin+cols[col][row]
  source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'785','0','0'],stderr=subprocess.DEVNULL))
  for row in range(4):
   e=source['events'][str(9+row*3+col)]
   assert 'blindstepGemPuzzle(get_character(0))' in str(e['list']) and e['trigger']==0
  for row,target in enumerate(cols[col]):
   eid=str(9+row*3+col);current=nav['positions']['785'][eid][0];count=origin+target-current
   if not count:continue
   run('q',f'785,{current-1},{11+row}')
   start=(785,current-1,11+row);assert locate(785)==start
   # Face with a reliable bump into the adjacent impassable tuner. A .03s
   # tap can miss polling and leave the player facing the previous route.
   act('right:.18','wait:.3')
   log(column=col,row=row,pending_pushes=count)
   act(*[k for _ in range(count)for k in ['c:.18','wait:.45','right:.18','wait:.3']])
   observed=locate(785);assert observed==(785,origin-1+target,11+row),f'Push endpoint review: {observed}'
   log(column=col,row=row,verified_player=list(observed),inferred_tuner=[origin+target,11+row],basis='Exactly N action-button pushes, N vacated-square moves, and observed player endpoint')
   planner=R/'notes/navigation-state.json';v=json.loads(planner.read_text());v['positions']['785'][eid]=[origin+target,11+row];planner.write_text(json.dumps(v)+'\n')
  label=f'VictoryRoad186-gem1-column{col+1}';run('checkpoint',label);n=R/'notes'/f'{label}-navigation.json'
  nav=json.loads(n.read_text())
  for row,count in enumerate(cols[col]):assert nav['positions']['785'][str(9+row*3+col)]==[origin+count,11+row]
  log(column=col,frozen_checkpoint=label,all_four_tuner_positions_verified=True)
 print('ALL TWELVE CRYSTALS VERIFIED; ask Cal to check solution',flush=True)
if __name__=='__main__':main()
