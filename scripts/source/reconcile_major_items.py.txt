"""Reconcile one or two retained major victories against frozen native saves.

Supply only completed logs and public closed-victory attempt records. Reads no
live game/logs or future battle decisions; writes only an optional new report.
Glass122–124 must continue using reconcile_glass_items.py and its chain proof.
"""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

from reconcile_glass_items import ROOT, reconcile, file_evidence, bind_native_chain

IDENTITY_FIELDS=('id','session','attempt','interaction_start_epoch','battle_start_epoch','battle_end_epoch','victory_epoch','result')


def attempt_identity(row):
    identity={key:row[key]for key in IDENTITY_FIELDS}
    if identity['result']!='victory':raise ValueError('Retained battle attempt must be a completed victory')
    if any(type(identity[key])is not int or identity[key]<1 for key in ['id','session','attempt']):
        raise ValueError('Major ID/session/attempt must be positive integers')
    times=[identity[key]for key in ['interaction_start_epoch','battle_start_epoch','victory_epoch','battle_end_epoch']]
    if not all(type(value)in[int,float] and math.isfinite(value)for value in times) or not times[0]<=times[1]<times[2]<=times[3]:
        raise ValueError('Completed victory timestamps must be finite and chronological')
    # A recorded VS transition can precede pbStartBattle's log constructor.
    # Admit its later public challenge only when retained as explicit evidence.
    # Allow a brief review pause at the VS card (Lumi317: 34.5 seconds).
    if 'battle_challenge_epoch' in row:
        ep=row['battle_challenge_epoch'];evidence=row.get('battle_challenge_evidence',{})
        text=' '.join(evidence.get('text',[])).lower()
        if (type(ep)not in[int,float] or not math.isfinite(ep)
            or not times[1]<=ep<=min(times[1]+60,times[2])
            or evidence.get('epoch')!=ep or not re.search('[wmuv]ouldliketobattle',re.sub('[^a-z]','',text))
            or not row.get('opponent') or row['opponent'].lower()not in text):
            raise ValueError('Require the same opponent public challenge within one minute of its recorded VS entry')
        identity['battle_challenge_epoch']=ep
    return identity


def identity_sha256(identity):
    return hashlib.sha256(json.dumps(identity,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def completed_log_identity(path,identity,save_mtime):
    """Bind the native log's creation second to this observed battle entry.

    Battle.rb3625 constructs AI/log before scene3677 and challenge3679/3695.
    Battle_AI.rb125–136 writes the same local timestamp into filename/header.
    The truncation to seconds permits only the interaction's current second.
    """
    match=re.match(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}) - ',path.name)
    if not match:raise ValueError('Keep the completed native log timestamp filename')
    zone=datetime.fromisoformat(save_mtime).tzinfo
    if zone is None:raise ValueError('Frozen native status needs its local timezone offset')
    created=datetime.strptime(match[1],'%Y-%m-%d_%H-%M-%S').replace(tzinfo=zone).timestamp()
    upper=identity.get('battle_challenge_epoch',identity['battle_start_epoch'])
    if not math.floor(identity['interaction_start_epoch'])<=created<=upper:
        raise ValueError('Completed log creation is outside this retained battle entry')
    lines=path.read_text().splitlines();ending=' - '+path.stem
    if not lines or not lines[0].endswith(ending) or sum(line.endswith(ending)for line in lines)!=1:
        raise ValueError('Require one native battle header matching the completed log filename')
    return {'created_epoch':created,'native_timestamp':match[1],'timezone_offset':str(zone)}


def build_report(before_path,after_path,logs,saves,attempt_paths,major_ids):
    """Return a report; no file mutation and no automatic log discovery."""
    count=len(logs)
    if count not in [1,2] or len(attempt_paths)!=count or len(major_ids)!=count:
        raise ValueError('Supply one or two logs with one major ID and attempt-record path per log')
    if len(set(logs))!=count or len(set(major_ids))!=count:
        raise ValueError('Completed logs and retained major IDs must be distinct')
    if any(mid in [122,123,124]for mid in major_ids):
        raise ValueError('Glass122–124 requires its three-round reconciliation helper and chain proof')
    before,after=[json.loads(path.read_text())for path in [before_path,after_path]]
    report=reconcile(before,after,[path.read_text()for path in logs],expected_rounds=count)
    report.update(reconciliation_kind='major_battles',
                  scope='Consumed player bag items in the supplied retained major victories',
                  assumptions=['Logs contain player bag executions; review NPC/reusable attribution separately',
                               'No tracked-consumable shopping, rewards, field use, held loss or other outside flow'],
                  does_not_prove=['Absence of outside bag flows beyond the reviewed checkpoint protocol'])
    report['evidence']={'before':file_evidence(before_path),'after':file_evidence(after_path),
                        'completed_logs':[file_evidence(path)for path in logs]}
    bind_native_chain(report,before,after,saves,None)
    identities=[];records=[]
    for number,(mid,path,log,row)in enumerate(zip(major_ids,attempt_paths,logs,report['per_round']),1):
        attempts=json.loads(path.read_text())
        winners=[attempt for attempt in attempts if attempt.get('id')==mid and attempt.get('result')=='victory']
        if not winners:raise ValueError(f'No completed victorious attempt for major{mid} in {path}')
        selected=winners[-1]
        if selected.get('gauntlet_id')=='glass':raise ValueError('Glass requires the whole-chain helper')
        identity=attempt_identity(selected);identities.append(identity)
        log_identity=completed_log_identity(log,identity,before['save_mtime'])
        # Hash only stable retained-battle identity, so unrelated future entries
        # may be appended to this same public recording journal.
        records.append({'path':file_evidence(path)['path'],'identity':identity,
                        'identity_sha256':identity_sha256(identity)})
        row.update(major_id=mid,battle_session=identity['session'],battle_attempt=identity['attempt'],
                   battle_start_epoch=identity['battle_start_epoch'],battle_end_epoch=identity['battle_end_epoch'],
                   victory_epoch=identity['victory_epoch'],completed_log_sha256=file_evidence(log)['sha256'],
                   completed_log_identity=log_identity)
    if not all(a['battle_end_epoch']<b['battle_start_epoch']for a,b in zip(identities,identities[1:])):
        raise ValueError('Supplied victories must be in chronological order without overlap')
    pre,post=[datetime.fromisoformat(status['save_mtime']).timestamp()for status in [before,after]]
    if pre>identities[0]['interaction_start_epoch'] or post<identities[-1]['battle_end_epoch']:
        raise ValueError('Pre/post native snapshots must enclose all supplied victories')
    report['evidence']['attempt_records']=records
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('before',type=Path);p.add_argument('after',type=Path)
    p.add_argument('completed_logs',type=Path,nargs='+')
    p.add_argument('--major-id',type=int,action='append',required=True,help='Repeat for a second log/major')
    p.add_argument('--attempts',type=Path,action='append',required=True,help='Repeat in log order; public winning-attempt JSON')
    p.add_argument('--before-save',type=Path,required=True);p.add_argument('--after-save',type=Path,required=True)
    p.add_argument('--output',type=Path,help='Optional new JSON report inside this repository')
    a=p.parse_args();before,after=a.before.resolve(),a.after.resolve()
    logs=[path.resolve()for path in a.completed_logs]
    saves=[a.before_save.resolve(),a.after_save.resolve()]
    records=[path.resolve()for path in a.attempts]
    inputs=[before,after,*logs,*saves,*records]
    if any(not path.is_relative_to(ROOT)for path in inputs):p.error('All inputs must be frozen/public evidence inside this repository')
    if len(set([before,after,*logs,*saves]))!=4+len(logs) or any(path.suffix!='.rxdata'for path in saves):
        p.error('Require distinct status/log/native-save files and .rxdata native copies')
    output=a.output.resolve()if a.output else None
    if output and (not output.is_relative_to(ROOT) or output.suffix!='.json' or output in inputs or output.exists()):
        p.error('--output must be a new separate JSON report inside this repository')
    try:report=build_report(before,after,logs,saves,records,a.major_id)
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError)as error:p.error(str(error))
    encoded=json.dumps(report,indent=2)+'\n'
    if output:
        output.parent.mkdir(parents=True,exist_ok=True);output.write_text(encoded)
    print(encoded,end='')
    return 0 if report['status']=='verified_counts'else 1


if __name__=='__main__':raise SystemExit(main())
