"""Enter Victory Road puzzle 2's clue-derived solution using ordinary controls.
Only a fresh legitimate puzzle checkpoint is accepted. Each bounded push group
is checked via public coordinates; every column is saved normally and the owned
frozen event positions are checked. No hidden answer or game writes are used.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('journal');p.add_argument('--start-column',type=int,default=0,choices=range(4));a=p.parse_args()
 n=R/'notes'/f'{a.label}-navigation.json'; s=R/'notes'/f'{a.label}-status.json';j=R/a.journal
 assert not j.exists() and time.time()-n.stat().st_mtime<120
 assert json.loads(s.read_text())['map']==789
 sol=json.loads((R/'work/196-gem-puzzle2-solution.json').read_text())['solutions'];assert len(sol)==1
 cols=[sol[0][k]for k in ['size','hardness','purity','foliation']]
 from play import act,read
 from locate import locate
 history=[]
 def log(**kw):history.append(dict(epoch=time.time(),**kw));j.write_text(json.dumps(history,indent=2)+'\n')
 def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True)
 for col in range(a.start_column,4):
  nav=json.loads(n.read_text());origin=16+6*col
  for row in range(4):
   xx,yy=nav['positions']['789'][str(5+row*4+col)]
   assert yy==12+row and origin<=xx<=origin+cols[col][row]
  source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),'789','0','0'],stderr=subprocess.DEVNULL))
  for row in range(4):
   e=source['events'][str(5+row*4+col)]
   assert 'blindstepGemPuzzle(get_character(0))' in str(e['list']) and e['trigger']==0
  for row,target in enumerate(cols[col]):
   eid=str(5+row*4+col);current=nav['positions']['789'][eid][0];count=origin+target-current
   if not count:continue
   run('q',f'789,{current-1},{12+row}')
   start=(789,current-1,12+row);assert locate(789)==start
   # Face with a reliable bump into the adjacent impassable tuner. A .03s
   # tap can miss polling and leave the player facing the previous route.
   act('right:.18','wait:.3')
   log(column=col,row=row,pending_pushes=count)
   act(*[k for _ in range(count)for k in ['c:.18','wait:.45','right:.18','wait:.3']])
   observed=locate(789);assert observed==(789,origin-1+target,12+row),f'Push endpoint review: {observed}'
   log(column=col,row=row,verified_player=list(observed),inferred_tuner=[origin+target,12+row],basis='Exactly N action-button pushes, N vacated-square moves, and observed player endpoint')
   planner=R/'notes/navigation-state.json';v=json.loads(planner.read_text());v['positions']['789'][eid]=[origin+target,12+row];planner.write_text(json.dumps(v)+'\n')
  label=f'VictoryRoad196-gem2-column{col+1}';run('checkpoint',label);n=R/'notes'/f'{label}-navigation.json'
  nav=json.loads(n.read_text())
  for row,count in enumerate(cols[col]):assert nav['positions']['789'][str(5+row*4+col)]==[origin+count,12+row]
  log(column=col,frozen_checkpoint=label,all_four_tuner_positions_verified=True)
 print('ALL SIXTEEN CRYSTALS VERIFIED; ask Hardy to check solution',flush=True)
if __name__=='__main__':main()
