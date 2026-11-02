"""Guarded UI-only Luna opener. Importing this module performs no game input.

Run only at the first command menu of Glass round 2: Lv90 Arcanine vs Lv83
Weavile. This queues eight reviewed X items, healing when necessary, and never
selects a move. A pending journal means the last item requires manual review.
"""
from __future__ import annotations

import argparse
import difflib
import json
import pathlib
import re
import subprocess
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = pathlib.Path('/Applications/Reborn.app/Contents/Game')
# Calibrated from an existing screencapture -l native image, not SCK points.
# The shadowed retina image has its title bar at y76..131 and game at y132.
CAPTURE_CANVASES = {(2272, 1816): (112, 132, 2048, 1536),
                    (1024, 796): (0, 28, 1024, 768)}
SETUP = ('X Defend', 'X Speed', 'X Defend', 'X Sp.Def', 'X Sp.Def',
         'X Sp.Atk', 'X Sp.Atk', 'X Sp.Atk')
TRANSLATION = str.maketrans({'р': 'p', 'у': 'y', 'а': 'a', 'о': 'o',
                           'с': 'c', 'е': 'e', 'х': 'x', 'к': 'k',
                           'і': 'i', 'ј': 'j', 'п': 'n'})


def normalized(text):
    text = unicodedata.normalize('NFKD', text.lower().translate(TRANSLATION))
    return re.sub('[^a-z0-9]', '', text.encode('ascii', 'ignore').decode())


def named(text, expected):
    words = re.findall('[a-z]+', text.lower().translate(TRANSLATION))
    aliases = {'weavile': ('weavile', 'weauile'),
               'arcanine': ('arcanine', 'arcamine', 'areanine')}
    return any(normalized(word) in aliases[expected] or
               difflib.SequenceMatcher(None, expected, normalized(word)).ratio() >= .84
               for word in words)


def level_seen(text, expected):
    # Normalize only a labelled level token, never arbitrary HUD numbers.
    # The actual outlined Lv90 glyph was read as Lụ9o: ụ is u after NFKD and
    # the final o is a zero only within this explicit numeric level context.
    plain = unicodedata.normalize('NFKD', text.lower().translate(TRANSLATION))
    plain = plain.encode('ascii', 'ignore').decode()
    tokens = re.findall(r'\bl[vu][ .:]*([0-9oq]{1,3})\b', plain)
    return any(int(token.replace('o', '0').replace('q', '0')) == expected
               for token in tokens)


def hp_pair(text, expected_max):
    # Accept only an explicit fraction. Do not turn a level or two isolated
    # numbers into HP, nor guess an unreadable digit.
    pairs = {(int(a), int(b)) for a, b in
             re.findall(r'(?<!\d)(\d{1,3})\s*/\s*(\d{2,3})(?!\d)', text)}
    pairs = {(hp, total) for hp, total in pairs
             if total == expected_max and 0 < hp <= total}
    if len(pairs) != 1:
        raise RuntimeError('Numeric HP is missing, ambiguous, zero, or has an unexpected maximum')
    return next(iter(pairs))


@dataclass(frozen=True)
class VisibleState:
    hp: int
    total_hp: int
    status: str
    bar_fraction: float
    status_error: float
    hud_y_offset: int
    boosts: tuple
    boost_icon_error: float
    own_text: str
    foe_text: str


class Queue:
    def __init__(self, args):
        # play is the only imported helper. Legacy battle helpers execute at
        # import time, so invoke those as bounded subprocesses instead.
        import play
        from PIL import Image
        self.play, self.Image, self.args = play, Image, args
        self.canvas = args.canvas
        self.journal_path = args.journal
        if args.prior_journal is not None:
            self.journal = args.prior_journal
            self.journal.setdefault('initial_guard_stop_history', []).append({
                'stop_epoch': self.journal.pop('stop_epoch', None),
                'stop_reason': self.journal.pop('stop_reason', None),
                'resume_epoch': time.time()})
        else:
            self.journal = {'created_epoch': time.time(), 'policy': 'ordinary rendered UI only',
                            'setup': list(SETUP), 'expected_actor': 'Arcanine Lv90',
                            'expected_foe': 'Weavile Lv83', 'actions': [], 'pending': None,
                            'complete': False}
        self.journal['expected_max_hp'] = args.expected_max_hp
        self.heals = self.cures = self.actions = 0
        self.templates = self.status_templates()
        # Battle_Scene.pbGetStatsBoostsDisplayMap: accuracy, attack, Sp.Atk,
        # speed, defense, Sp.Def, evasion. Round 2 must begin with zero stages.
        self.stages = [0] * 7
        self.write()

    def write(self):
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.journal_path.with_suffix(self.journal_path.suffix + '.tmp')
        tmp.write_text(json.dumps(self.journal, indent=2) + '\n')
        tmp.replace(self.journal_path)

    def status_templates(self):
        Image = self.Image
        assets = GAME / 'Graphics/Pictures/Battle'
        # Battle_Scene.rb: player box base=(34,0), badge=(baseX+24,36).
        background = Image.open(assets / 'battlePlayerBoxS.png').convert('RGBA')
        background = background.crop((58, 36, 122, 52))
        badges = Image.open(assets / 'battleStatuses.png').convert('RGBA')
        templates = {'none': background.convert('RGB')}
        for i, status in enumerate(('sleep', 'poison', 'burn', 'paralysis', 'frozen')):
            layer = badges.crop((0, 16 * i, 64, 16 * (i + 1)))
            templates[status] = Image.alpha_composite(background, layer).convert('RGB')
        return templates

    def crop(self, native, rect):
        left, top, width, height = self.canvas
        x1, y1, x2, y2 = rect
        return native.crop((round(left + x1 * width / 512),
                            round(top + y1 * height / 384),
                            round(left + x2 * width / 512),
                            round(top + y2 * height / 384)))

    def ocr_crop(self, native, rect, stem):
        crop = self.crop(native, rect)
        crop = crop.resize((crop.width * 3, crop.height * 3),
                           self.Image.Resampling.NEAREST)
        path = ROOT / 'work' / ('luna-setup-' + stem + '.png')
        crop.save(path)
        result = subprocess.run([str(ROOT / 'scripts/observe'), str(path)],
                                check=True, capture_output=True, text=True, timeout=20)
        return '\n'.join(row['text'] for row in json.loads(result.stdout))

    def status(self, native):
        # Compare actual rendered badge pixels to all five installed sprites
        # and the blank databox. Absence of an OCR status word is not evidence
        # of healthy status. Small color conversion errors are tolerated.
        errors = []
        for name, template in self.templates.items():
            offsets = []
            # PokemonDataBox.update bobs the selected box down two game pixels.
            # Compare both legal positions rather than mistaking that animation
            # for a healthy badge or for an unexpected status.
            for dy in (0, 2):
                seen = self.crop(native, (326, 228 + dy, 390, 244 + dy)).convert('RGB')
                scaled = template.resize(seen.size, self.Image.Resampling.NEAREST)
                distance = sum(sum(abs(a - b) for a, b in zip(p, q))
                               for p, q in zip(seen.getdata(), scaled.getdata()))
                offsets.append((distance / (seen.width * seen.height * 3), dy))
            error, dy = min(offsets)
            errors.append((error, name, dy))
        errors.sort()
        if errors[0][0] > 20 or errors[1][0] - errors[0][0] < 2:
            raise RuntimeError('Status badge or HUD geometry is uncertain: ' + repr(errors))
        return errors[0][1], round(errors[0][0], 3), errors[0][2]

    def hp_bar(self, native, dy):
        # PBScene.rb: player x=268, baseX=34, gauge x=102,y=40,w=96.
        bar = self.crop(native, (404, 233 + dy, 500, 237 + dy)).convert('RGB')
        filled = []
        for x in range(bar.width):
            colored = 0
            for y in range(bar.height):
                r, g, b = bar.getpixel((x, y))
                if (g > 75 and g > r * 1.3 and g > b * 1.3) or (
                        r > 130 and b < 85 and g < 220):
                    colored += 1
            filled.append(colored / max(1, bar.height) > .45)
        if not any(filled):
            raise RuntimeError('HP bar is not visible at the reviewed single-battle HUD position')
        # An HP fill must begin at the left and form a contiguous prefix.
        end = max(i for i, value in enumerate(filled) if value) + 1
        if sum(filled[:end]) / end < .95:
            raise RuntimeError('HP bar has unexpected gaps; HUD geometry is uncertain')
        return end / bar.width

    def boost_icons(self, native, dy):
        # pbGetStatsBoostsTabCoords: x=268+28-50=246, y=192-4=188.
        # The 22x22 stage sprites overlap in the installed draw order; compare
        # the complete composite rather than independent overlapping cells.
        assets = GAME / 'Graphics/Pictures/Battle'
        background = self.Image.open(assets / 'statdis1.png').convert('RGBA')
        sprites = self.Image.open(assets / 'statdis2.png').convert('RGBA')
        positions = ((14, 0), (2, 10), (26, 10), (14, 20),
                     (2, 30), (26, 30), (14, 40))
        def composite(stages):
            panel = background.copy()
            for stage, position in zip(stages, positions):
                if stage:
                    x = 0 if stage > 0 else 22
                    y = (abs(stage) - 1) * 22
                    icon = sprites.crop((x, y, x + 22, y + 22))
                    panel.alpha_composite(icon, dest=position)
            return panel
        def score_pixels(actual_pixels, stages):
            errors = [sum(abs(a - b) for a, b in zip(actual, expected[:3])) / 3
                      for actual, expected in zip(actual_pixels, composite(stages).getdata())
                      if expected[3] == 255]
            if not errors:
                raise RuntimeError('Installed boost icon template has no opaque pixels')
            return sum(errors) / len(errors)
        # A blank healthy-status background can tie at both bob offsets. Locate
        # the boost panel independently rather than inheriting that arbitrary
        # tie choice. Only the two source-authorized positions are considered.
        candidates = []
        for offset in (dy, 2 - dy):
            seen = self.crop(native, (246, 188 + offset, 296, 252 + offset)).convert('RGB')
            # Sample original sprite resolution; retina pixels repeat.
            seen = seen.resize(background.size, self.Image.Resampling.NEAREST)
            pixels = list(seen.getdata())
            candidates.append((score_pixels(pixels, self.stages), offset, pixels))
        _, _, actual_pixels = min(candidates, key=lambda value: value[:2])
        def score(stages):
            return score_pixels(actual_pixels, stages)
        error = score(self.stages)
        if error > 18:
            raise RuntimeError('Visible boost panel does not prove expected stages '
                               + repr(self.stages) + '; error=' + str(round(error, 2)))
        # An absolute whole-panel threshold alone could accept an unchanged
        # small icon. Require the expected stage in each cell to beat every
        # alternate legal -6..+6 value, including the pre-item stage.
        for position in range(7):
            rivals = []
            for stage in range(-6, 7):
                if stage == self.stages[position]:
                    continue
                candidate = self.stages.copy()
                candidate[position] = stage
                rivals.append((score(candidate), stage))
            alternate_error, alternate = min(rivals)
            if alternate_error - error < .15:
                raise RuntimeError('Boost icon is ambiguous or disagrees in cell '
                                   + str(position) + ': expected ' + str(self.stages[position])
                                   + ', alternate ' + str(alternate) + ', error gap '
                                   + str(round(alternate_error - error, 3)))
        return round(error, 3)

    def guard_once(self):
        rows = self.play.snap()
        text = '\n'.join(row['text'] for row in rows)
        low = text.lower().translate(TRANSLATION)
        labels={normalized(row['text']) for row in rows}
        if not {'fight','bag'} <= labels or not labels.intersection({'run','riun'}):
            raise RuntimeError('Exact battle command menu expected; no navigation attempted')
        if any(word in low for word in ('fainted', 'switch in', 'change pok', 'for winning',
                                       'out of usable', 'no energy left', 'choose a pok')):
            raise RuntimeError('Unexpected battle transition or replacement prompt')
        prompt = ' '.join(row['text'] for row in rows if row['y'] > .72 and row['x'] < .55)
        if not named(prompt, 'arcanine'):
            raise RuntimeError('Command prompt does not independently identify Arcanine')
        native = self.Image.open(self.play.NATIVE).convert('RGB')
        if self.canvas is None:
            self.canvas = CAPTURE_CANVASES.get(native.size)
            if self.canvas is None:
                raise RuntimeError('Uncalibrated native screenshot size; supply a verified --canvas: '
                                   + repr(native.size))
            self.journal['canvas'] = list(self.canvas)
            self.journal['native_image_size'] = list(native.size)
            self.write()
        left, top, width, height = self.canvas
        if left < 0 or top < 0 or width <= 0 or height <= 0 or (
                left + width > native.width or top + height > native.height):
            raise RuntimeError('Configured game content rectangle is outside the captured window')
        if abs(width / height - 4 / 3) > .01:
            raise RuntimeError('Expected a 4:3 game canvas')
        own = self.ocr_crop(native, (268, 192, 512, 281), 'own-hud')
        foe = self.ocr_crop(native, (0, 30, 256, 112), 'foe-hud')
        if not named(own, 'arcanine') or not level_seen(own, 90):
            raise RuntimeError('Own HUD is not unambiguously Arcanine Lv90: ' + own)
        if not named(foe, 'weavile') or not level_seen(foe, 83):
            wide_foe='\n'.join(row['text'] for row in rows if row['y']<.37 and row['x']<.5)
            if not named(wide_foe,'weavile') or not level_seen(wide_foe,83):
                raise RuntimeError('Foe HUD is not unambiguously Weavile Lv83: ' + foe+'; widerHUD='+wide_foe)
            foe=wide_foe
        hp, total = hp_pair(own, self.args.expected_max_hp)
        status, error, dy = self.status(native)
        fraction = self.hp_bar(native, dy)
        if abs(fraction - hp / total) > .045:
            raise RuntimeError('Numeric HP disagrees with the rendered HP bar')
        if status not in ('none', 'poison'):
            raise RuntimeError('Unexpected status requires manual review: ' + status)
        boost_error = self.boost_icons(native, dy)
        return VisibleState(hp, total, status, round(fraction, 4), error, dy,
                            tuple(self.stages), boost_error, own, foe)

    def guard(self):
        first = self.guard_once()
        time.sleep(.2)
        second = self.guard_once()
        if (first.hp, first.total_hp, first.status) != (second.hp, second.total_hp, second.status):
            raise RuntimeError('Two rendered-UI reads disagree; HP/status may still be animating')
        return second

    def public_evidence(self, offset):
        path = ROOT / 'recordings/screens.jsonl'
        with path.open('rb') as handle:
            handle.seek(offset)
            lines = handle.read(2_000_000).decode('utf-8').splitlines()
        return ['\n'.join(json.loads(line)['text']) for line in lines if line.strip()]

    def proof(self, item, evidence, before, after):
        compact = [normalized(text) for text in evidence]
        if any('noeffect' in text or 'wonthaveanyeffect' in text or
               'cantbeused' in text or 'cannotbeused' in text
               for text in compact):
            raise RuntimeError('Rendered item failure message; do not repeat automatically')
        if item.startswith('X '):
            stat = {'X Defend': ('defense', 'defence'), 'X Speed': ('speed',),
                    'X Sp.Def': ('spdef', 'specialdefense', 'specialdefence'),
                    'X Sp.Atk': ('spatk', 'spattack', 'specialattack')}[item]
            matching = [text for text in evidence if named(text, 'arcanine') and
                        any(s in normalized(text) for s in stat) and
                        any(s in normalized(text) for s in ('rose', 'raised', 'sharply'))]
            # Turbo can finish these brief non-paused messages before the item
            # helper's next screenshot. Both stable HUD reads must instead
            # prove the exact source-rendered panel transition in that case.
            if before.boosts == after.boosts:
                raise RuntimeError('X item did not produce a proved boost-panel transition')
            matching.append('RENDERED BOOST PANEL: ' + repr(before.boosts) +
                            ' -> ' + repr(after.boosts) +
                            '; exact installed sprite composite matched twice')
        elif item == 'Ultra Potion':
            matching = [text for text in evidence if any(s in normalized(text)
                        for s in ('restored', 'recovered', 'regained'))]
            if after.hp > before.hp:
                # Charcoal Arcanine vs these four damaging Weavile moves has
                # no passive HP recovery. A stable numeric/bar-confirmed HP
                # increase independently proves the ordinary heal resolved.
                matching.append('RENDERED HP INCREASE: ' + str(before.hp) +
                                ' -> ' + str(after.hp))
        else:
            matching = [text for text in evidence if any(s in normalized(text)
                        for s in ('cured', 'healed', 'healthy', 'poisoning'))]
            if before.status == 'poison' and after.status == 'none':
                matching.append('RENDERED STATUS BADGE: poison -> none')
        if not matching:
            raise RuntimeError('Item effect was not proved by rendered UI; review the pending action')
        return list(dict.fromkeys(matching))[:6]

    def use(self, item, state, setup_index=None):
        if self.actions >= self.args.max_actions:
            raise RuntimeError('Total item action budget reached')
        if item == 'Ultra Potion' and self.heals >= self.args.max_heals:
            raise RuntimeError('Ultra Potion budget reached')
        if item == 'Full Heal' and self.cures >= self.args.max_cures:
            raise RuntimeError('Full Heal budget reached')
        path = ROOT / 'recordings/screens.jsonl'
        offset = path.stat().st_size
        pending = {'item': item, 'setup_index': setup_index, 'before': asdict(state),
                   'start_epoch': time.time(), 'public_ui_offset': offset}
        self.journal['pending'] = pending
        self.write()
        command = [sys.executable, str(ROOT / 'scripts/battle_item.py'), item, 'Arcanine']
        if item.startswith('X '):
            command.append('--active')
        else:
            command.extend(('--pocket', 'Medicine'))
        print('QUEUED', item, 'HP', state.hp, '/', state.total_hp, state.status, flush=True)
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        pending['helper_stdout_tail'] = result.stdout[-3500:]
        pending['helper_stderr_tail'] = result.stderr[-1500:]
        pending['returncode'] = result.returncode
        self.write()
        if result.returncode:
            raise RuntimeError('Bounded named-item helper stopped; pending action requires manual review')
        # This helper selects no move. It only advances stable turn messages,
        # cancels an accidental move grid, and stops at the command menu.
        ready = subprocess.run([sys.executable, str(ROOT / 'scripts/battle_ready.py')],
                               capture_output=True, text=True, timeout=180)
        pending['ready_returncode'] = ready.returncode
        self.write()
        if ready.returncode:
            raise RuntimeError('Turn readiness stopped; pending action requires manual review')
        evidence = self.public_evidence(offset)
        if item.startswith('X '):
            index = {'X Defend': 4, 'X Speed': 3, 'X Sp.Def': 5, 'X Sp.Atk': 2}[item]
            self.stages[index] += 2
            if self.stages[index] > 6:
                raise RuntimeError('Reviewed setup would exceed maximum stage; no automatic replay')
        after = self.guard()
        pending['effect_ui_proof'] = self.proof(item, evidence, state, after)
        if item == 'Full Heal' and after.status == 'poison':
            # The same opposing Poison Jab can poison again. Stop for review
            # instead of silently asserting a cure or spending repeated cures.
            raise RuntimeError('Poison remains after Full Heal; possible immediate re-poisoning')
        pending['after'] = asdict(after)
        pending['end_epoch'] = time.time()
        self.journal['actions'].append(pending)
        self.journal['pending'] = None
        self.actions += 1
        self.heals += item == 'Ultra Potion'
        self.cures += item == 'Full Heal'
        self.write()
        return after

    def safe(self, state):
        while state.hp < 180 or state.status == 'poison':
            # Bag heals happen before the opponent's attack. Cure only once HP
            # meets the reviewed safety floor; cure never outranks HP recovery.
            item = 'Ultra Potion' if state.hp < 180 else 'Full Heal'
            state = self.use(item, state)
        return state

    def run(self):
        state = self.guard()
        self.journal['initial'] = asdict(state)
        self.write()
        for index, item in enumerate(SETUP):
            state = self.safe(state)
            # Reconfirm actor, exact foe, HP and status immediately before each
            # fixed setup item, including after an inserted potion or cure.
            state = self.guard()
            if state.hp < 180 or state.status != 'none':
                raise RuntimeError('Safety state changed before setup action')
            state = self.use(item, state, index)
        state = self.safe(state)
        self.journal['final'] = asdict(state)
        self.journal['complete'] = True
        self.journal['finished_epoch'] = time.time()
        self.journal['boosts_proved'] = {'defense': 4, 'speed': 2,
                                        'special_defense': 4, 'special_attack': 6}
        self.write()
        print('SETUP COMPLETE — stopped at command menu before attacking; HP',
              state.hp, '/', state.total_hp, 'status', state.status, flush=True)


def canvas_arg(text):
    try:
        values = tuple(int(value) for value in text.split(','))
        if len(values) != 4:
            raise ValueError
        return values
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Canvas must be left,top,width,height') from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-max-hp', type=int, default=294)
    parser.add_argument('--canvas', type=canvas_arg,
                        help='Verified native-pixel left,top,width,height; default uses calibrated '
                             '2272x1816 shadowed-retina or 1024x796 unshadowed capture presets')
    parser.add_argument('--journal', type=pathlib.Path,
                        default=ROOT / 'notes/luna-arcanine-setup-run.json')
    parser.add_argument('--max-actions', type=int, default=22)
    parser.add_argument('--max-heals', type=int, default=8)
    parser.add_argument('--max-cures', type=int, default=6)
    parser.add_argument('--resume-initial-guard', action='store_true',
                        help='Retry the same untouched opening only if the journal has no '
                             'initial state, actions, pending item or completion')
    args = parser.parse_args()
    args.prior_journal = None
    if args.journal.exists():
        if not args.resume_initial_guard:
            raise SystemExit('Journal already exists. Review it; do not automatically replay setup items. '
                             'Use a fresh journal only for a genuinely new round-2 opening.')
        prior = json.loads(args.journal.read_text())
        if ('initial' in prior or prior.get('actions') != [] or
                prior.get('pending') is not None or prior.get('complete') is not False):
            raise SystemExit('Initial-guard retry refused: this journal may have advanced gameplay')
        if (prior.get('setup') != list(SETUP) or
                prior.get('expected_actor') != 'Arcanine Lv90' or
                prior.get('expected_foe') != 'Weavile Lv83' or
                prior.get('expected_max_hp', args.expected_max_hp) != args.expected_max_hp):
            raise SystemExit('Initial-guard retry refused: journal policy/build does not match')
        args.prior_journal = prior
    elif args.resume_initial_guard:
        raise SystemExit('Initial-guard retry requires the existing stopped journal')
    if not 290 <= args.expected_max_hp <= 310:
        raise SystemExit('Unexpected Arcanine maximum HP; review the actual build')
    queue = None
    try:
        queue = Queue(args)
        queue.run()
    except (RuntimeError, subprocess.SubprocessError, OSError, ValueError, KeyError) as exc:
        if queue is not None:
            queue.journal['stop_epoch'] = time.time()
            queue.journal['stop_reason'] = str(exc)
            queue.write()
        raise SystemExit('STOP — ' + str(exc)) from exc


if __name__ == '__main__':
    main()
