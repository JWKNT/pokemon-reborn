"""Enter Victory Road puzzle 3 or 4's clue-derived solution using ordinary controls.
Only a fresh legitimate puzzle checkpoint is accepted. Each bounded push group
is checked via public coordinates; every column is saved normally and the owned
frozen event positions are checked. No hidden answer or game writes are used.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('puzzle',type=int,choices=[3,4]);p.add_argument('label');p.add_argument('journal');p.add_argument('--start-column',type=int,default=0,choices=range(6));a=p.parse_args()
 mid,base,columns,origin0,row0={3:(793,9,5,20,18),4:(795,14,6,17,23)}[a.puzzle]
 assert a.start_column<columns
 n=R/'notes'/f'{a.label}-navigation.json'; s=R/'notes'/f'{a.label}-status.json';j=R/a.journal
 assert not j.exists() and time.time()-n.stat().st_mtime<120
 assert json.loads(s.read_text())['map']==mid
 sol=json.loads((R/f'work/198-gem-puzzle{a.puzzle}-solution.json').read_text())['solutions'];assert len(sol)==1
 cols=[sol[0][k]for k in ['size','hardness','purity','foliation','luster','habit'][:columns]]
 from play import act,read
 from locate import locate
 history=[]
 def log(**kw):history.append(dict(epoch=time.time(),**kw));j.write_text(json.dumps(history,indent=2)+'\n')
 def run(name,*args):subprocess.run([sys.executable,str(R/'scripts'/f'{name}.py'),*map(str,args)],check=True)
 for col in range(a.start_column,columns):
  nav=json.loads(n.read_text());origin=origin0+6*col
  for row in range(4):
   xx,yy=nav['positions'][str(mid)][str(base+row*columns+col)]
   assert yy==row0+row and origin<=xx<=origin+cols[col][row]
  source=json.loads(subprocess.check_output(['ruby',str(R/'scripts/route_map.rb'),str(mid),'0','0'],stderr=subprocess.DEVNULL))
  for row in range(4):
   e=source['events'][str(base+row*columns+col)]
   assert 'blindstepGemPuzzle(get_character(0))' in str(e['list']) and e['trigger']==0
  for row,target in enumerate(cols[col]):
   eid=str(base+row*columns+col);current=nav['positions'][str(mid)][eid][0];count=origin+target-current
   if not count:continue
   run('q',f'{mid},{current-1},{row0+row}')
   start=(mid,current-1,row0+row);assert locate(mid)==start
   # Face with a reliable bump into the adjacent impassable tuner. A .03s
   # tap can miss polling and leave the player facing the previous route.
   act('right:.18','wait:.3')
   log(column=col,row=row,pending_pushes=count)
   act(*[k for _ in range(count)for k in ['c:.18','wait:.45','right:.18','wait:.3']])
   observed=locate(mid);assert observed==(mid,origin-1+target,row0+row),f'Push endpoint review: {observed}'
   log(column=col,row=row,verified_player=list(observed),inferred_tuner=[origin+target,row0+row],basis='Exactly N action-button pushes, N vacated-square moves, and observed player endpoint')
   planner=R/'notes/navigation-state.json';v=json.loads(planner.read_text());v['positions'][str(mid)][eid]=[origin+target,row0+row];planner.write_text(json.dumps(v)+'\n')
  label=f'{a.label}-column{col+1}';run('checkpoint',label);n=R/'notes'/f'{label}-navigation.json'
  nav=json.loads(n.read_text())
  for row,count in enumerate(cols[col]):assert nav['positions'][str(mid)][str(base+row*columns+col)]==[origin+count,row0+row]
  log(column=col,frozen_checkpoint=label,all_four_tuner_positions_verified=True)
 print('ALL CRYSTALS VERIFIED; use the normal Check Solution choice',flush=True)
if __name__=='__main__':main()
