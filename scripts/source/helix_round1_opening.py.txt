"""Four reviewed opening turns, using public menus and existing input guards."""
from play import *

journal = json.loads((ROOT / 'notes/active-league-chain.json').read_text())
assert journal['kind'] == 'helix' and journal['status'] == 'active'
assert journal['rounds'] == [], 'Only the first round opening is approved'
receipt = ROOT / 'notes' / (journal['run_id'] + '-opening.json')
assert not receipt.exists(), 'Opening already started; inspect its receipt and resume manually'
progress = dict(run_id=journal['run_id'], started_epoch=time.time(), completed_turns=[])
receipt.write_text(json.dumps(progress, indent=2) + '\n')

def command(actor):
    subprocess.run([sys.executable, str(ROOT / 'scripts/battle_ready.py')], check=True)
    rows = snap()
    text = ' '.join(v['text'] for v in rows).lower()
    compact = re.sub('[^a-z]', '', text)
    expected = re.sub('[^a-z]', '', actor.lower())
    if actor == 'Meowstic':
        compact = compact.replace('meoustic', 'meowstic')
    assert 'fight' in text and expected in compact, 'Opening actor/menu changed: ' + text
    assert not any(w in text for w in ['fainted', 'choose a pok', 'defeated']), text

steps = [
    ('Meowstic', 'battle_move', '1', '--watch'),
    ('Meowstic', 'battle_switch', 'Magearna'),
    ('Magearna', 'battle_item', 'X Defend', 'Magearna'),
    ('Magearna', 'battle_move', '3', '--watch'),
]
for turn, (actor, helper, *args) in enumerate(steps, 1):
    command(actor)
    if turn == 1:
        text = read().lower()
        assert 'ninetales' in text and 'glaceon' in text, 'Initial opponents changed'
    print('HELIX OPENING TURN', turn, helper, *args, flush=True)
    progress['pending_turn'] = turn
    receipt.write_text(json.dumps(progress, indent=2) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'scripts' / (helper + '.py')), *args], check=True)
    progress['completed_turns'].append(turn)
    progress['pending_turn'] = None
    receipt.write_text(json.dumps(progress, indent=2) + '\n')
command('Magearna')
progress['finished_epoch'] = time.time()
receipt.write_text(json.dumps(progress, indent=2) + '\n')
print('OPENING COMPLETE; review the current opposing lineup before attacking', flush=True)
