"""Enter a real Bag/party screen, or briefly inspect the world and re-pause.

Uses only normal keys and newly recorded public pixels. The pause command list
is deliberately never accepted as a frozen world. Before the challenge, open
Bag normally once so the remembered pause-menu choice is Bag.
"""
import argparse,json,time,shutil
from pathlib import Path

def classify(rows):
    words=[r['text'].strip().lower() for r in rows]
    text=' '.join(words)
    if any(k in text for k in ['what will','fight','quit game','would you like']):return None
    if ('sort' in text and any(k in text for k in ['medicine','items','berries','close bag'])):return 'bag'
    if 'cancel' in text and (text.count('hp')>=5 or sum(n in text for n in ['arcanine','swampert','cofagrigus','klinklang','sylveon','excadrill'])>=4) and any(k in text for k in ['choose a pok','chooce a pok','thoose a pok']):return 'party'
    return None

def finish_bag_entry():
    """Verify a requested pause and recover the fresh-load Pokédex default."""
    from play import act,snap
    rows=snap();text=' '.join(v['text'] for v in rows).lower()
    if 'quit game' in text:
        act('c:.12','wait:1.2');rows=snap();text=' '.join(v['text'] for v in rows).lower()
    if 'pokedex' in text and 'search' in text:
        act('x:.12','wait:1','down:.12','wait:.2','down:.12','wait:.2','c:.12','wait:1.2')
        rows=snap()
    assert classify(rows)=='bag','Actual Bag entry requires immediate review'
    return rows

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['open','peek','verify']);a=p.parse_args()
    from play import act,snap,ROOT,NATIVE
    if a.mode=='peek':
        assert classify(snap())=='bag','Peek requires the actual main Bag screen'
        act('x:.12','wait:1','x:.12','wait:.4')
        rows=snap();epoch=time.time()
        world=ROOT/'work/chest-world-observation.png';shutil.copy2(NATIVE,world)
        if any(x['y']>.72 and len(x['text'])>8 for x in rows):
            (ROOT/'work/chest-world-observation.json').write_text(json.dumps({'epoch':epoch,'rows':rows,'image':str(world),'interruption':'public dialogue; no confirmation sent'},indent=2))
            print('DIALOGUE INTERRUPTED PEEK; no Bag claim and no further inputs',flush=True)
            raise SystemExit(2)
        # Return immediately to the remembered Bag before doing any analysis.
        act('x:.12','wait:.3','c:.12','wait:1.5')
        (ROOT/'work/chest-world-observation.json').write_text(json.dumps({'epoch':epoch,'rows':rows,'image':str(world)},indent=2))
    elif a.mode=='open':
        act('x:.12','wait:.3','c:.12','wait:1.5')
    rows=snap();kind=classify(rows)
    assert kind, 'Actual Bag/party pause was NOT verified; inspect the current screen promptly'
    proof={'epoch':time.time(),'screen':kind,'rows':rows,'basis':'Public rendered full-screen Bag/party; installed pbFadeOutIn blocks map updates'}
    (ROOT/'work/chest-pause-proof.json').write_text(json.dumps(proof,indent=2))
    print('ACTUAL WORLD PAUSE VERIFIED',kind,flush=True)
    if a.mode=='peek':print(world,flush=True)
if __name__=='__main__':main()
