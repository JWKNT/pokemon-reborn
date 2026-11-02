"""Source-only Lyla/Ezra opening plan; never executes UI or reads live state.

Optional --status/--navigation read explicitly named frozen staging evidence.
Public intro, transform, actor and target verification are still required by
the sole root controller before entering the printed normal commands.
"""
import argparse
import hashlib
import json
from pathlib import Path
from calcenon_agate_queue import need
from trainer_enter import installed_event,validate_pair

ROOT=Path(__file__).resolve().parents[1]
GAME=Path('/Applications/Reborn.app/Contents/Game')


def source_proof():
    primary=installed_event(763,45);paired=installed_event(763,46)
    proof=validate_pair(primary['pages'][0]['list'],paired['pages'][0]['list'],
                        45,46,'NWCultistF','Lyla & Ezra')
    trainers=(GAME/'Scripts/Trainers.rb').read_text()
    battle=(GAME/'Scripts/Battle.rb').read_text()
    battler=(GAME/'Scripts/Battler.rb').read_text()
    need('combinedParty[i] = $PokemonTemp.waitingTrainer[0][2][i]' in trainers and
         'combinedParty[6 + i] = trainer[2][i]' in trainers and
         '[$PokemonTemp.waitingTrainer[0][0], trainer[0]]' in trainers,
         'Waiting-trainer order changed')
    need('@battlers[1].pbInitialize(@party2[sendout1], sendout1, false)' in battle and
         '@battlers[3].pbInitialize(@party2[sendout2], sendout2, false)' in battle and
         'choice = pkmn.pbOppositeOpposing' in battle and '@index ^ 3' in battler,
         'Source enemy slot/Imposter geometry changed')
    proof.update(opponents=['Lyla:Noivern@index1','Ezra:Ditto@index3'],
                 own=['Cryogonal@index0','Mienshao@index2'],ditto_copies_own_slot=0,
                 prerequisite='reviewed simultaneous overlap; no old waiting trainer; both undefeated',
                 source_order_note='notes/agate-double-order-source-proof-2026-10-03.md')
    return proof


def staging_proof(status,nav):
    need(status['map']==763 and status['position'][1]>=53 and nav['variables']['391']==52,
         'Reviewed normal southern prechain staging required')
    need(nav.get('self_switches',{}).get('763,49,A') is True,
         'Actual Antoine victory required')
    need(not any(nav.get('self_switches',{}).get(f'763,{e},A',False) for e in [45,46]),
         'Both Lyla/Ezra must remain undefeated')
    party=status['party']
    need(len(party)==6 and {m['species'] for m in party}==
         {'CRYOGONAL','MIENSHAO','COFAGRIGUS','ARCANINE','SWAMPERT','EXCADRILL'},
         'Reviewed final six required')
    cryo,mien=party[:2]
    need(cryo['species']=='CRYOGONAL' and cryo['name']=='Hexan' and
         mien['species']=='MIENSHAO','Cryo first/Mien second is required for Ditto pairing')
    need(all(m['level']==90 and m['hp']==m['totalhp'] and m['status'] is None for m in party),
         'Normal nurse/full HP/status-free final six required')
    need(cryo['totalhp']==320 and cryo['speed']==207 and cryo['item']=='FOCUSSASH' and
         [m['move'] for m in cryo['moves']]==['LIGHTSCREEN','ICEBEAM','RECOVER','FREEZEDRY'] and
         cryo['moves'][1]['pp']>0,
         'Actual Cryo build/Sash/IceBeam slot1 differs')
    need(mien['speed']==217 and mien['moves'][2]['move']=='FAKEOUT' and mien['moves'][2]['pp']>0,
         'Actual Mienshao speed/FakeOut slot2 differs')
    return {'frozen_staging_only':True,'position':status['position'],'lead_order':['Hexan','Mienshao']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--status',type=Path);p.add_argument('--navigation',type=Path)
    a=p.parse_args();out={'source_only':True,'no_controls':True,'source':source_proof(),
        'public_gates':['Lyla and Ezra actual intro','Noivern and Ditto exact HUDs',
            'Ditto visibly transforms into Hexan/Cryogonal before first action',
            'fresh Hexan command before first move; fresh Mienshao command before second',
            'actual physical target HUDs match Noivern(index1)/Ditto(index3)'],
        'registration_order':[
            {'actor':'Hexan','move':'Ice Beam','slot':1,'target':'Noivern','battler_index':1,
             'command':['python3','scripts/battle_move.py','1','1','--foe-names','Noivern,Ditto','--watch']},
            {'actor':'Mienshao','move':'Fake Out','slot':2,'target':'Ditto','battler_index':3,
             'command':['python3','scripts/battle_move.py','2','3','--foe-names','Noivern,Ditto','--watch']}],
        'resolution':'FakeOut priority3 acts before Noivern; ordinary UI registers Cryo first, Mien second.',
        'after_turn':'Stop for actual public messages/HP/status/foe pair. No automatic retry/nextturn.'}
    if a.status or a.navigation:
        need(a.status and a.navigation,'Pass both explicit frozen staging paths')
        need(a.status.resolve().is_relative_to(ROOT) and a.navigation.resolve().is_relative_to(ROOT),
             'Frozen evidence must stay in workspace')
        out['staging']=staging_proof(json.loads(a.status.read_text()),json.loads(a.navigation.read_text()))
        out['binding']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [a.status,a.navigation]}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
