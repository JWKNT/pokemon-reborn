"""Reconcile three completed Glass logs with native pre/post-chain bag snapshots.

Reads only the explicitly supplied files. It never finds or reads a live log,
changes a game/save/manifest, or allocates aggregate refunds to individual rounds.
The caller must prove that the logs are completed consecutive winning rounds and
that tracked consumables had no shopping, field uses, rewards or other bag flows.
"""
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
# Exact installed Reborn itemtext.rb IDs/names; all are one-unit consumables.
# In particular X Sp. Atk is XSPECIAL, not XSPATK.
CONSUMABLES = {
    'POTION': 'Potion', 'SUPERPOTION': 'Super Potion',
    'HYPERPOTION': 'Hyper Potion', 'ULTRAPOTION': 'Ultra Potion',
    'MAXPOTION': 'Max Potion', 'FULLRESTORE': 'Full Restore',
    'LEMONADE': 'Lemonade',
    'AWAKENING': 'Awakening', 'ANTIDOTE': 'Antidote',
    'BURNHEAL': 'Burn Heal', 'PARLYZHEAL': 'Paralyze Heal',
    'ICEHEAL': 'Ice Heal', 'FULLHEAL': 'Full Heal',
    'REVIVE': 'Revive', 'MAXREVIVE': 'Max Revive',
    'COTTONCANDY': 'Cotton Candy', 'REVIVALHERB': 'Revival Herb',
    'XATTACK': 'X Attack', 'XDEFEND': 'X Defend',
    'XSPECIAL': 'X Sp. Atk', 'XSPDEF': 'X Sp. Def',
    'XSPEED': 'X Speed', 'XACCURACY': 'X Accuracy',
    'DIREHIT': 'Dire Hit', 'GUARDSPEC': 'Guard Spec.',
    'ETHER': 'Ether', 'MAXETHER': 'Max Ether',
    'ELIXIR': 'Elixir', 'MAXELIXIR': 'Max Elixir',
}
NAME_TO_ID = {name: item for item, name in CONSUMABLES.items()}
EXECUTION = re.compile(r'^\[Player used (.+)\]\s*$', re.M)
STORY_ITEMS = {'SAPPHIREBRACELETS'}


def native_inventory(status):
    """Use PokemonBag.contents, which native pbQuantity reads directly."""
    bag = status.get('bag', {})
    contents = bag.get('contents')
    if bag.get('type') != 'PokemonBag' or not isinstance(contents, dict):
        raise ValueError('Expected native status JSON bag.type=PokemonBag and bag.contents')
    if any(type(qty) is not int or qty < 0 for qty in contents.values()):
        raise ValueError('Native bag quantities must be nonnegative integers')
    party = status.get('party')
    if not isinstance(party, list) or not all(isinstance(mon, dict) and 'item' in mon for mon in party):
        raise ValueError('Native party held-item fields are required')
    held = Counter(mon['item'] for mon in party if mon['item'])
    return contents, held


def reconcile(before, after, completed_logs, expected_rounds=3):
    if type(expected_rounds)is not int or expected_rounds<1 or len(completed_logs)!=expected_rounds:
        raise ValueError(f'Exactly {expected_rounds} completed logs are required, in battle order')
    pre, pre_held = native_inventory(before)
    post, post_held = native_inventory(after)
    rounds = [Counter(EXECUTION.findall(text)) for text in completed_logs]
    total = sum(rounds, Counter())
    errors = []
    unknown = sorted(set(total) - set(NAME_TO_ID))
    if unknown:
        errors.append({'reason': 'Unknown or reusable executed item; scope must be reviewed', 'names': unknown})

    aggregate = []
    for item, name in CONSUMABLES.items():
        qty_before, qty_after = pre.get(item, 0), post.get(item, 0)
        delta = qty_before - qty_after
        executions = total[name]
        held_changed = pre_held[item] != post_held[item]
        if executions or delta or held_changed:
            aggregate.append({'item_id': item, 'name': name,
                              'logged_executions': executions,
                              'bag_before': qty_before, 'bag_after': qty_after,
                              'bag_decline': delta,
                              'held_before': pre_held[item], 'held_after': post_held[item],
                              'matched': delta == executions and not held_changed})
        if held_changed:
            errors.append({'item_id': item, 'reason': 'Tracked consumable held stock changed; cannot infer transfer versus other loss'})
        if delta != executions:
            errors.append({'item_id': item, 'reason': 'Bag decline does not equal executed-use markers',
                           'bag_decline': delta, 'logged_executions': executions})

    ignored = []
    for item in sorted(set(pre) | set(post)):
        delta = pre.get(item, 0) - post.get(item, 0)
        if delta and item not in CONSUMABLES:
            held_change = post_held[item] - pre_held[item]
            category = ('story_key_item' if item in STORY_ITEMS else
                        'held_transfer_candidate' if held_change == delta else
                        'outside_tracked_consumable_scope')
            ignored.append({'item_id': item, 'bag_decline': delta,
                            'held_change': held_change, 'excluded_as': category})

    per_round = []
    for i, counts in enumerate(rounds, 1):
        row = {'round': i, 'logged_executions': [
            {'name': name, 'count': count} for name, count in sorted(counts.items())]}
        # All markers are consumption only when the entire chain balances and
        # the stated no-other-flow assumptions hold. Never guess refund rounds.
        if not errors:
            row['item_usage'] = row['logged_executions']
        per_round.append(row)
    return {'status': 'mismatch' if errors else 'verified_counts',
            'scope': f'Player bag consumables in the {expected_rounds} supplied completed battles',
            'assumptions': ['Supplied logs are completed and player-only; Glass has no NPC partner',
                            'Snapshots anchor this exact uninterrupted winning chain',
                            'No tracked-consumable shopping, rewards, field use, held loss or other outside flow'],
            'does_not_prove': ['Victory or chain continuity', 'Whole-gauntlet attempt count'],
            'per_round': per_round, 'aggregate': sorted(aggregate, key=lambda row: row['name']),
            'ignored_bag_changes': ignored, 'errors': errors,
            'mismatch_policy': 'Review per-round visible no-effect/refund ledger; never distribute aggregate differences by guessing'}


def file_evidence(path):
    path=path.resolve()
    display=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    return {'path': display, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def read_saved_inventory(path):
    """Read a frozen native save through RGSS stubs; never load the game runtime."""
    code="v=load_rgss(ARGV[0]); t=v[:Trainer]; puts JSON.generate({bag:plain(v[:PokemonBag]),party:t.instance_variable_get(:@party).map { |m| {item:m.instance_variable_get(:@item)} }})"
    return json.loads(subprocess.check_output(
        ['ruby','-r',str(Path(__file__).with_name('read_rgss.rb')),'-e',code,str(path)],
        text=True,stderr=subprocess.DEVNULL))


def bind_native_chain(report, before, after, saves, proof_path):
    """Attach source provenance for later staging; all inputs are frozen files."""
    for status,save in zip([before,after],saves):
        if native_inventory(status)!=native_inventory(read_saved_inventory(save)):
            raise ValueError('Status JSON bag/held inventory differs from its frozen native save: '+str(save))
    report['evidence']['native_saves']={key:file_evidence(path) for key,path in zip(['before','after'],saves)}
    report['native_save_inventories_verified']=True
    if proof_path is None:return
    proof=json.loads(proof_path.read_text()); rounds=proof.get('rounds',[])
    if [r.get('id')for r in rounds]!=[122,123,124]:
        raise ValueError('Expected completed Glass chain proof rounds122,123,124')
    if proof.get('native_checkpoint_sha256')!=report['evidence']['native_saves']['before']['sha256']:
        raise ValueError('Pre-chain native save does not match the completed-chain checkpoint proof')
    if not all(r['start']<r['end']for r in rounds) or not all(a['end']<b['start']for a,b in zip(rounds,rounds[1:])):
        raise ValueError('Completed-chain proof rounds are not chronological')
    if datetime.fromisoformat(before['save_mtime']).timestamp()>rounds[0]['start']:
        raise ValueError('Pre-chain snapshot was saved after round1 started')
    if datetime.fromisoformat(after['save_mtime']).timestamp()<rounds[-1]['end']:
        raise ValueError('Post-chain snapshot was saved before round3 ended')
    report['evidence']['chain_proof']=file_evidence(proof_path)
    report['gauntlet_run_id']=proof['run_id']
    for row,source,log in zip(report['per_round'],rounds,report['evidence']['completed_logs']):
        row.update(major_id=source['id'],battle_start_epoch=source['start'],
                   battle_end_epoch=source['end'],completed_log_sha256=log['sha256'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('before', type=Path)
    p.add_argument('after', type=Path)
    p.add_argument('completed_logs', type=Path, nargs=3, metavar='ROUND_LOG')
    p.add_argument('--output', type=Path, help='Optional new JSON report inside this repository')
    p.add_argument('--before-save',type=Path,help='Frozen pre-chain .rxdata copy inside this repository')
    p.add_argument('--after-save',type=Path,help='Frozen post-chain .rxdata copy inside this repository')
    p.add_argument('--chain-proof',type=Path,help='Completed Glass chain verification JSON; requires both native save copies')
    a = p.parse_args()
    paths = [a.before.resolve(), a.after.resolve(), *[path.resolve() for path in a.completed_logs]]
    if len(set(paths)) != len(paths):
        p.error('Before/after snapshots and all three completed logs must be distinct files')
    output = a.output.resolve() if a.output else None
    if output and (not output.is_relative_to(ROOT) or output in paths or output.suffix != '.json'):
        p.error('--output must be a separate JSON report inside this repository')
    if output and output.exists():
        p.error('--output already exists; preserve prior evidence or choose a new report path')
    if bool(a.before_save)!=bool(a.after_save) or a.chain_proof and not a.before_save:
        p.error('Provide both --before-save and --after-save; --chain-proof requires both')
    saves=[a.before_save.resolve(),a.after_save.resolve()] if a.before_save else []
    proof=a.chain_proof.resolve() if a.chain_proof else None
    if any(not path.is_relative_to(ROOT) or path.suffix!='.rxdata' for path in saves):
        p.error('Native save inputs must be frozen .rxdata copies inside this repository')
    if proof and not proof.is_relative_to(ROOT):p.error('Chain proof must be inside this repository')
    if len(set(saves))!=len(saves) or output and output in saves+[proof]:
        p.error('Native save copies and output report must be distinct files')
    try:
        before,after=[json.loads(path.read_text())for path in paths[:2]]
        report = reconcile(before,after,[path.read_text() for path in paths[2:]])
        report['evidence'] = {'before': file_evidence(paths[0]), 'after': file_evidence(paths[1]),
                              'completed_logs': [file_evidence(path) for path in paths[2:]]}
        if saves:bind_native_chain(report,before,after,saves,proof)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        p.error(str(exc))
    encoded = json.dumps(report, indent=2) + '\n'
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded)
    print(encoded, end='')
    return 0 if report['status'] == 'verified_counts' else 1


if __name__ == '__main__':
    raise SystemExit(main())
