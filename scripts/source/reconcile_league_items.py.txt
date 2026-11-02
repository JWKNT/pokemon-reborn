"""Balance a completed seven-round League with explicitly evidenced field uses.

Only frozen saves, completed logs and closed public journals are inputs.
No UI, live-log discovery, or game/save writes.
"""
import argparse,copy,hashlib,json
from pathlib import Path
from datetime import datetime
from collections import Counter
from reconcile_glass_items import ROOT,CONSUMABLES,reconcile,native_inventory,read_saved_inventory,file_evidence
from reconcile_major_items import attempt_identity,identity_sha256,completed_log_identity

def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def resolve(root,p):return (Path(root)/p).resolve()

FIELD_ONLY_ITEMS={'REPEL','SUPERREPEL','MAXREPEL'}

def adjusted_before(before,field):
    adjusted=copy.deepcopy(before);totals=Counter()
    for row in field:
        assert row['item'] in set(CONSUMABLES)|FIELD_ONLY_ITEMS and type(row['count']) is int and row['count']>0
        assert type(row['after_round']) is int and 1<=row['after_round']<=6
        assert row['target'] in {m['name'] for m in before['party']} or (row['item'] in FIELD_ONLY_ITEMS and row['target']=='field')
        totals[row['item']]+=row['count']
    for item,n in totals.items():
        assert adjusted['bag']['contents'].get(item,0)>=n
        adjusted['bag']['contents'][item]-=n
    return adjusted,dict(sorted(totals.items()))

def build_report(before_path,after_path,logs,saves,chain_path,attempt_paths,field_path,root=ROOT,native_reader=read_saved_inventory):
    root=Path(root).resolve();before,after=map(read,(before_path,after_path));chain=read(chain_path);field=read(field_path)
    assert chain['kind']=='hard-route-league' and chain['status']=='completed'
    assert len(logs)==len(attempt_paths)==len(chain['rounds'])==7 and len(set(logs))==7
    assert len(saves)==2 and saves[0]!=saves[1] and sha(saves[0])==chain['save_sha256']
    assert sha(before_path)==chain['preentry_status_sha256']
    assert [r['id']for r in chain['rounds']]==list(range(136,143))
    assert all(r['result']=='victory' for r in chain['rounds'])
    for status,path in zip((before,after),saves):assert native_inventory(status)==native_inventory(native_reader(path))
    adjusted,field_totals=adjusted_before(before,field)
    report=reconcile(adjusted,after,[p.read_text()for p in logs],expected_rounds=7)
    records=[];identities=[];field_evidence=[]
    for row in field:
        p=resolve(root,row['evidence']);assert p.is_relative_to(root) and p.is_file()
        field_evidence.append(file_evidence(p))
    for number,(r,path,log,out) in enumerate(zip(chain['rounds'],attempt_paths,logs,report['per_round']),1):
        matches=[a for a in read(path) if a.get('id')==r['id'] and a.get('gauntlet_run_id')==chain['run_id']]
        assert len(matches)==1;a=matches[0];ident=attempt_identity(a)
        assert a['gauntlet_id']=='hard-route-league' and a['gauntlet_round']==number and a['gauntlet_completed'] is True
        assert a['gauntlet_attempts']==chain['attempt'] and a['continuity_proof']['save_sha256']==chain['save_sha256']
        for k in ('id','session','result','battle_start_epoch','battle_end_epoch'):assert r[k]==ident[k]
        identities.append(ident);records.append({'path':file_evidence(path)['path'],'identity':ident,'identity_sha256':identity_sha256(ident)})
        out.update(major_id=r['id'],completed_log_sha256=sha(log),completed_log_identity=completed_log_identity(log,ident,before['save_mtime']))
    assert all(a['battle_end_epoch']<b['battle_start_epoch'] for a,b in zip(identities,identities[1:]))
    assert datetime.fromisoformat(before['save_mtime']).timestamp()<=identities[0]['interaction_start_epoch']
    assert datetime.fromisoformat(after['save_mtime']).timestamp()>=identities[-1]['battle_end_epoch']
    report.update(reconciliation_kind='hard_route_league',gauntlet_run_id=chain['run_id'],whole_gauntlet_attempts=chain['attempt'],native_save_inventories_verified=True,
        field_item_totals=field_totals,scope='Seven victorious battle consumable totals; separately evidenced between-round medicines excluded',
        assumptions=['The reviewed field-use ledger contains all between-round tracked consumable uses.', 'No tracked-consumable rewards, purchases or other outside flows.', 'Player execution markers only; all seven completed public victories bound to this no-save chain.'])
    for row in report['aggregate']:
        row['field_uses']=field_totals.get(row['item_id'],0)
        row['native_bag_before']=before['bag']['contents'].get(row['item_id'],0)
    report['evidence']={'before':file_evidence(before_path),'after':file_evidence(after_path),'completed_logs':[file_evidence(p)for p in logs],
        'native_saves':dict(zip(('before','after'),map(file_evidence,saves))),'chain':file_evidence(chain_path),'field_ledger':file_evidence(field_path),
        'field_use_evidence':field_evidence,'attempt_records':records}
    return report

def verified_league_item_usage(config,attempt,item_log,root=ROOT):
    root=Path(root).resolve();assert config.get('gauntlet_id')==attempt.get('gauntlet_id')=='hard-route-league'
    number=config['gauntlet_round'];assert number==attempt['gauntlet_round']==config['item_usage_reconciliation_round'] and 1<=number<=7
    path=resolve(root,config['item_usage_reconciliation']);assert path.is_relative_to(root);report=read(path)
    assert report['status']=='verified_counts' and report['errors']==[]
    def checked(e):
        p=resolve(root,e['path']);assert p.is_relative_to(root) and sha(p)==e['sha256'];return p
    e=report['evidence'];before,after=map(checked,(e['before'],e['after']));logs=list(map(checked,e['completed_logs']));saves=[checked(e['native_saves'][k])for k in ('before','after')]
    chain,field=map(checked,(e['chain'],e['field_ledger']));list(map(checked,e['field_use_evidence']))
    paths=[resolve(root,r['path'])for r in e['attempt_records']];assert all(p.is_relative_to(root)for p in paths)
    for r in e['attempt_records']:assert identity_sha256(r['identity'])==r['identity_sha256']
    assert attempt_identity(attempt)==e['attempt_records'][number-1]['identity']
    assert resolve(root,item_log)==logs[number-1]
    assert report['gauntlet_run_id']==config['gauntlet_run_id']==attempt['gauntlet_run_id']
    assert report['whole_gauntlet_attempts']==config['gauntlet_attempts']==attempt['gauntlet_attempts']
    assert build_report(before,after,logs,saves,chain,paths,field,root)==report
    row=report['per_round'][number-1];assert row['major_id']==config['id']
    return row['item_usage'],{'source':str(logs[number-1].relative_to(root)),'method':'Completed seven-round League logs reconciled against frozen native stock after deducting evidenced field medicines',
        'scope':'Player battle consumables only; field medicines excluded','reconciliation':str(path.relative_to(root)),'reconciliation_sha256':sha(path),'gauntlet_run_id':report['gauntlet_run_id'],'round':number,'whole_gauntlet_attempts':report['whole_gauntlet_attempts']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('spec',type=Path);p.add_argument('output',type=Path);a=p.parse_args();spec=read(a.spec);assert not a.output.exists()
    one=lambda k:resolve(ROOT,spec[k]);many=lambda k:[resolve(ROOT,x)for x in spec[k]]
    r=build_report(one('before'),one('after'),many('logs'),many('saves'),one('chain'),many('attempts'),one('field'))
    a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status']);raise SystemExit(0 if r['status']=='verified_counts' else 1)
