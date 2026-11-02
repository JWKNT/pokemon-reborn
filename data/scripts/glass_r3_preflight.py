"""Read rendered R3 doubles HUD, emit guarded opener plan; sends no game keys.

Development validation is syntax-only. Invoke at an actual command menu, then
run the printed JSON plan separately with glass_turn.py if the root approves
the observed report. Unknown replacements, status or a damaged opening stop.
"""
import argparse
import difflib
import json
import math
import pathlib
import re
import subprocess
import time

from PIL import Image
from play import ROOT, NATIVE, snap
from luna_arcanine_setup import CAPTURE_CANVASES, TRANSLATION, level_seen, normalized

ASSETS = pathlib.Path('/Applications/Reborn.app/Contents/Game/Graphics/Pictures/Battle')


def name_seen(text, name):
    words = re.findall('[a-z]+', text.lower().translate(TRANSLATION))
    return any(difflib.SequenceMatcher(None, normalized(name), normalized(word)).ratio() >= .82
               for word in words)


def crop(native, canvas, rect):
    left, top, width, height = canvas
    x1, y1, x2, y2 = rect
    return native.crop((round(left + x1 * width / 512), round(top + y1 * height / 384),
                        round(left + x2 * width / 512), round(top + y2 * height / 384)))


def ocr(native, canvas, rect, label):
    patch = crop(native, canvas, rect)
    patch = patch.resize((patch.width * 2, patch.height * 2), Image.Resampling.NEAREST)
    path = ROOT / 'work' / ('glass-r3-' + label + '.png')
    patch.save(path)
    value = subprocess.run([str(ROOT / 'scripts/observe'), str(path)], check=True,
                           capture_output=True, text=True, timeout=20)
    return '\n'.join(row['text'] for row in json.loads(value.stdout))


def status_and_hp(native, canvas, x, y, maximum):
    blank = Image.open(ASSETS / 'battlePlayerBoxD.png').convert('RGBA').crop((58, 36, 122, 52))
    badges = Image.open(ASSETS / 'battleStatuses.png').convert('RGBA')
    templates = {'none': blank.convert('RGB')}
    for i, label in enumerate(('sleep', 'poison', 'burn', 'paralysis', 'frozen')):
        templates[label] = Image.alpha_composite(blank, badges.crop((0, 16*i, 64, 16*(i+1)))).convert('RGB')
    scores = []
    for label, template in templates.items():
        offsets = []
        for dy in (0, 2):
            patch = crop(native, canvas, (x+58, y+36+dy, x+122, y+52+dy)).convert('RGB')
            expected = template.resize(patch.size, Image.Resampling.NEAREST)
            error = sum(sum(abs(a-b) for a,b in zip(p,q)) for p,q in
                        zip(patch.getdata(), expected.getdata())) / (patch.width*patch.height*3)
            offsets.append((error, dy))
        error, dy = min(offsets)
        scores.append((error, label, dy))
    scores.sort()
    if scores[0][0] > 20 or scores[1][0] - scores[0][0] < 2:
        raise RuntimeError('Ambiguous rendered doubles status badge: ' + repr(scores))
    if scores[0][1] != 'none':
        raise RuntimeError('Status requires manual cure/review: ' + scores[0][1])
    dy = scores[0][2]
    bar = crop(native, canvas, (x+136, y+41+dy, x+232, y+45+dy)).convert('RGB')
    columns = []
    for xx in range(bar.width):
        colored = 0
        for yy in range(bar.height):
            r,g,b = bar.getpixel((xx, yy))
            colored += (g > 75 and g > r*1.3 and g > b*1.3) or (r > 130 and b < 85 and g < 220)
        columns.append(colored / bar.height > .45)
    if not any(columns):
        raise RuntimeError('No visible HP fill; critical KO, missing HUD or unknown geometry')
    end = max(i for i,v in enumerate(columns) if v) + 1
    if sum(columns[:end]) / end < .95:
        raise RuntimeError('HP fill is not a contiguous prefix')
    units = end / bar.width * 96
    # Source truncates HP to a 96-pixel gauge and uses at least two pixels for
    # any positive HP. Report an interval rather than inventing exact HP.
    lower = 1 if units <= 2.25 else math.ceil((units-.25) * maximum / 96)
    upper = min(maximum, math.ceil((units+1.25) * maximum / 96) - 1)
    if units >= 95.75:
        lower = maximum
    return {'hp_lower': lower, 'hp_upper': upper, 'max_hp_assumed': maximum,
            'bar_units': round(units, 3), 'status': 'none', 'status_error': round(scores[0][0], 3)}


def read_guard(args):
    rows = snap()
    text = '\n'.join(row['text'] for row in rows)
    tokens = {normalized(row['text']) for row in rows}
    if 'fight' not in tokens or 'bag' not in tokens or not tokens & {'run', 'riun'}:
        raise RuntimeError('Exact command labels required; no keys sent')
    if any(phrase in text.lower() for phrase in ('fainted', 'switch in', 'choose a pok',
                                                'for winning', 'out of usable', 'change pok')):
        raise RuntimeError('Battle transition/replacement requires manual review')
    prompt = ' '.join(row['text'] for row in rows if row['y'] > .72 and row['x'] < .55)
    if not name_seen(prompt, args.actor):
        raise RuntimeError('Acting Pokémon is not the requested actor: ' + prompt)
    native = Image.open(NATIVE).convert('RGB')
    canvas = args.canvas or CAPTURE_CANVASES.get(native.size)
    if canvas is None:
        raise RuntimeError('Uncalibrated screenshot geometry; supply verified --canvas')
    left, top, width, height = canvas
    if left < 0 or top < 0 or left+width > native.width or top+height > native.height:
        raise RuntimeError('Canvas falls outside native screenshot')
    own = [('Arcanine', (256,172), args.arc_max_hp, (256,172,512,225)),
           ('Klinklang', (268,226), args.kg_max_hp, (268,226,512,280))]
    report = {}
    for name, position, maximum, rect in own:
        hud = ocr(native, canvas, rect, name.lower())
        if not name_seen(hud, name) or not level_seen(hud, 90):
            raise RuntimeError('Exact allied Lv90 HUD missing: ' + name + ' / ' + hud)
        report[name] = status_and_hp(native, canvas, *position, maximum)
        report[name]['hud_text'] = hud
    for name, rect in [('Clefable',(0,0,256,54)), ('Ninetales',(0,54,256,112))]:
        hud = ocr(native, canvas, rect, name.lower())
        if not name_seen(hud, name) or not level_seen(hud, 81):
            raise RuntimeError('Initial opposing slot changed; manual branch required: ' + name + ' / ' + hud)
        report[name] = {'level': 81, 'hud_text': hud}
    if args.phase == 't1':
        if report['Arcanine']['hp_lower'] != args.arc_max_hp or report['Klinklang']['hp_lower'] != args.kg_max_hp:
            raise RuntimeError('First-turn opener requires both allies fully healed')
    elif args.phase == 't2':
        if report['Arcanine']['hp_lower'] < 140 or report['Klinklang']['hp_lower'] < 130:
            raise RuntimeError('Turn-2 HP below ordinary reviewed opening branch; heal/adapt manually')
    elif report['Arcanine']['hp_lower'] < 140:
        raise RuntimeError('Arcanine too low to commit the reviewed support turn; adapt manually')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=('t1','t2','t3'), required=True)
    parser.add_argument('--actor', choices=('Arcanine','Klinklang'), default='Arcanine')
    parser.add_argument('--arc-max-hp', type=int, default=294)
    parser.add_argument('--kg-max-hp', type=int, default=275)
    parser.add_argument('--canvas', type=lambda s: tuple(map(int,s.split(','))))
    args = parser.parse_args()
    try:
        first = read_guard(args)
        time.sleep(.2)
        second = read_guard(args)
        for name in ('Arcanine','Klinklang'):
            if first[name]['bar_units'] != second[name]['bar_units']:
                raise RuntimeError('HP bar still changing between two rendered reads')
        plan = ROOT / 'work' / ('glass-r3-opener-' + args.phase + '.json')
        print(json.dumps({'phase': args.phase, 'actor': args.actor, 'visible': second,
                          'suggested_plan': str(plan), 'no_keys_sent': True}, indent=2))
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit('STOP — ' + str(exc)) from exc


if __name__ == '__main__':
    main()
