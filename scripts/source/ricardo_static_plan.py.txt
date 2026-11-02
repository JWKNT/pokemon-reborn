"""Bounded Ricardo1 static team/geometry proof; no gameplay or native access."""
import collections
import json
import math
from pathlib import Path

from glass_damage_review import damage

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = json.loads((ROOT / "work/ricardo-static-source.json").read_text())
    opponents = []
    rows = []
    for mon in source["team"][0]["mons"]:
        forms = [(name, data) for name, data in source["species"][mon["species"]].items()
                 if isinstance(data, dict) and name != "OnCreation"]
        # Battler.rb1489/2355: full-HP ShieldsDown Minior changes to Meteor7
        # on activation; the trainer's original YellowCore5 returns at halfHP.
        selected = 7 if mon["species"] == "MINIOR" else mon.get("form", 0)
        base = dict(forms[0][1])
        base.update(forms[selected][1])
        level = mon["level"]
        stats = [math.floor((2 * b + 10 + 21) * level / 100)
                 + (level + 10 if i == 0 else 5)
                 for i, b in enumerate(base["BaseStats"])]
        opponents.append(dict(mon, form_name=forms[selected][0], stats=stats))
        effectiveness = 2 if mon["species"] in ("MINIOR", "AGGRON", "BLAZIKEN") else 1
        rows.append(dict(target=mon["species"], move="Swamp+2Waterfall",
                         damage=damage(90, 80, 528, stats[2], base_modifier=1.2,
                                       modifier=1.5 * effectiveness), hp=stats[0]))
        if mon["species"] == "AGGRON":
            rows.append(dict(target="AGGRON", move="Swamp+2Earthquake",
                             damage=damage(90, 100, 528, stats[2], modifier=1.5 * 4),
                             hp=stats[0]))
        moves = {
            "SLURPUFF": [("PLAYROUGH", 90, "physical", 1.5, 1),
                         ("SURF", 90, "special", 1, 1)],
            "SCOLIPEDE": [("MEGAHORN", 120, "physical", 1.5, 1),
                          ("POISONJAB", 80, "physical", 1.5, .5),
                          ("ROCKSLIDE", 75, "physical", 1, .5)],
            "BLAZIKEN": [("HIJUMPKICK", 130, "physical", 1.5, 1),
                         ("FLAREBLITZ", 120, "physical", 1.5, .5),
                         ("BRAVEBIRD", 120, "physical", 1, 1),
                         ("ROCKSLIDE", 75, "physical", 1, .5)],
        }.get(mon["species"], [])
        for move, power, category, stab, eff in moves:
            attack = stats[1 if category == "physical" else 3]
            defense = 190 if category == "physical" else 183
            for critical in (False, True):
                rows.append(dict(enemy=mon["species"], move=move, target="SWAMPERT",
                                 critical=critical, damage=damage(
                                     level, power, attack, defense,
                                     modifier=stab * eff * (1.5 if critical else 1))))

    # Conservative union of all page obstacles/sightlines, never live flags.
    grid = source["map"]
    width, height = grid["width"], grid["height"]
    data, passages, priorities = (grid[k]["data"] for k in ("data", "passages", "priorities"))
    blocked, tile_events = set(), {}
    for event in grid["events"].values():
        pos = (event["x"], event["y"])
        for page in event["pages"]:
            graphic, commands = page["graphic"], page["list"]
            if not page["through"] and graphic["character_name"]:
                blocked.add(pos)
            if not page["through"] and graphic["tile_id"] > 0:
                tile_events.setdefault(pos, set()).add(graphic["tile_id"])
            if page["trigger"] in (1, 2) and any(c["code"] not in (0, 108, 408)
                                               for c in commands):
                blocked.add(pos)
            if "Trainer(" in event["name"] and any("pbTrainerBattle" in str(c["parameters"])
                                                  for c in commands):
                count = int(event["name"].split("(")[1].split(")")[0])
                dx, dy = {2: (0, 1), 4: (-1, 0), 6: (1, 0), 8: (0, -1)}[graphic["direction"]]
                blocked.update((event["x"] + dx * i, event["y"] + dy * i)
                               for i in range(1, count + 1))

    def passable(x, y, direction):
        if not (0 <= x < width and 0 <= y < height):
            return False
        bit = 1 << (direction // 2 - 1)
        for tile in tile_events.get((x, y), ()):
            if passages[tile] & bit or passages[tile] & 15 == 15:
                return False
            if priorities[tile] == 0:
                return True
        for z in (2, 1, 0):
            tile = data[x + width * y + width * height * z]
            if passages[tile] & bit or passages[tile] & 15 == 15:
                return False
            if priorities[tile] == 0:
                return True
        return True

    start, goal = (13, 54), (33, 61)
    queue = collections.deque([start])
    previous, directions = {start: None}, {}
    while queue:
        pos = queue.popleft()
        if pos == goal:
            break
        for dx, dy, direction, key in ((0, 1, 2, "down"), (-1, 0, 4, "left"),
                                       (1, 0, 6, "right"), (0, -1, 8, "up")):
            dest = (pos[0] + dx, pos[1] + dy)
            if (dest not in previous and dest not in blocked and passable(*pos, direction)
                    and passable(*dest, 10-direction)):
                previous[dest] = pos
                directions[dest] = key
                queue.append(dest)
    path = []
    if goal in previous:
        pos = goal
        while previous[pos] is not None:
            path.append(dict(position=list(pos), key=directions[pos]))
            pos = previous[pos]
        path.reverse()
    result = dict(proposal_only=True, executed=False, assumptions=(
        "Static installed Ricardo1, Hardy nature/10IV/85EV defaults. NoField, "
        "no AI, weather, drops, accuracy, or enemy future order prediction. "
        "Swamp90 295HP/264Atk/190Def/183SpDef/145Speed/WaveIncense."),
        opponents=opponents, damage=rows, route=dict(
            conservative_union_obstacles=True, found=bool(path), start=[763, *start],
            stop=[763, *goal], path=path, facing="down",
            forbidden=[[763, x, 62] for x in (30, 31, 32)]
            + [[763, x, 52] for x in range(43, 49)]))
    (ROOT / "work/ricardo-static-plan-proposal.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
